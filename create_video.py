import os
import pathlib
import shutil

import streamlit as st
from moviepy.editor import (
    ColorClip,
    CompositeVideoClip,
    ImageClip,
    TextClip,
    VideoFileClip,
    concatenate_videoclips,
)
from streamlit.elements.progress import ProgressMixin
from twitch_to_clip import dl_twitch


class StreamlitProgressBarLogger:
    progress_bar = st.progress(0)

    def __init__(self, message: str):
        st.text(str(message))

    @classmethod
    def initialize(cls, total):
        cls.progress_bar = st.progress(0)
        cls.total = total

    @classmethod
    def iter_bar(cls, **kw):
        for field, iterable in kw.items():
            text = "creating video" if str(field) == "t" else "processing chunks"
            cls.progress_bar = st.progress(0, text=text)
            for idx, i in enumerate(iterable):
                yield i
                cls.progress_bar.progress(idx / len(iterable), text=text)

    @classmethod
    def close(cls):
        if cls.progress_bar:
            cls.progress_bar.empty()


def create_video(links: list[str], title: str) -> str:
    """Get a list of links and generate a video from it."""
    check_links(links)
    temp_dir = pathlib.Path(pathlib.Path.cwd()) / "TEMP"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()

    video_files = []
    progress_dl = st.progress(0, text="Downloading clips")
    for i, clip in enumerate(links):
        clip_id = clip.split("/")[-1]

        clip_title, user, game, output_clip_name = dl_twitch.downloadTwitch(clip_id, None, [])
        clip_path = temp_dir / f"{i}_{output_clip_name}.mp4"
        shutil.move(f"raw_{output_clip_name}.mp4", clip_path)
        video_files.append((str(clip_path.resolve()), clip_title))
        progress_dl.progress((i + 1) / len(links), text="Downloading clips")

    file_name = create_video_from_clips(video_files, title=title)
    return file_name


def check_links(links: list[str]) -> None:
    for link in links:
        pass  # TODO


def create_video_from_clips(video_list: list[tuple[str, str]], title: str) -> str:
    clips = []
    for video_path, clip_title in video_list:
        clip = VideoFileClip(video_path, target_resolution=(1080, 1920))
        first_frame = clip.get_frame(0)
        first = ImageClip(first_frame)
        text_clip = TextClip(
            txt=clip_title.upper(),
            size=(0.8 * first_frame.shape[1], 0),
            font="Lane",
            color="black",
        )
        text_clip = text_clip.set_position("center")
        im_width, im_height = text_clip.size
        color_clip = ColorClip(size=(int(im_width * 1.1), int(im_height * 1.4)), color=(216, 255, 21))
        color_clip = color_clip.set_opacity(0.6)

        title_intro = CompositeVideoClip(
            [
                first,
                color_clip.set_position(("center", "center")),
                text_clip.set_position(("center", "center")),
            ]
        ).set_duration(2.5)
        title_intro = title_intro.set_position("center")

        clips.append(title_intro)
        clips.append(clip)

    final_clip = concatenate_videoclips(clips)
    video_dir = pathlib.Path(pathlib.Path.cwd()) / "VIDEO"
    if video_dir.exists():
        videos = list(video_dir.iterdir())
        if len(videos) > 1:
            for video in videos:
                video.unlink()
    else:
        video_dir.mkdir(parents=True, exist_ok=True)
    file_name = str(video_dir / f"{title}.mp4")
    final_clip.write_videofile(file_name, fps=60, logger=StreamlitProgressBarLogger)
    return file_name
