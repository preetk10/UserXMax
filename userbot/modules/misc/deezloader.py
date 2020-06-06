import os
import shutil

import deezloader

from userbot import userbot, Message
from ..help import add_help_item
from userbot import LOGS
from userbot.events import register

ARL_TOKEN = os.environ.get("ARL_TOKEN", None)
PATH = 'deezdown_temp/'
ARL_HELP = """**Oops, Time to Help Yourself**
[Here Help Yourself](https://www.google.com/search?q=how+to+get+deezer+arl+token)

After getting Arl token Config `ARL_TOKEN` var in heroku"""


@register(outgoing=True, pattern=r"^\.deezload(?: |$)(.*)")
async def deezload(message: Message):
    if not os.path.exists(PATH):
        os.makedirs(PATH)
    if not message.flags:
        await message.edit(
            "Check your E-Mail📧 I've sent an invitation to read help for DeezLoader :)")
        return
    await message.edit("Trying to Login 🥴")
    if ARL_TOKEN is None:
        await message.edit(ARL_HELP, disable_web_page_preview=True)
        return
    try:
        loader = deezloader.Login(ARL_TOKEN)
    except Exception as er:
        await message.edit(er)
        return

    flags = list(message.flags)
    if '-zip' not in flags:
        to_zip = False
    else:
        to_zip = True
    d_quality = "MP3_320"
    if not message.filtered_input_str:
        await message.edit("Bruh, Now I Think how far should we go. Plz Terminate my Session 🥺")
        return
    input_ = message.filtered_input_str
    if '-dsong' not in flags:
        try:
            input_link, quality = input_.split()
        except ValueError:
            if len(input_.split()) == 1:
                input_link = input_
                quality = d_quality
            else:
                await message.edit("🤔 Comedy? You are good at it")
                return
        if '.com' not in input_link:
            await message.edit("Invalid Link")
            return
    elif '-dsong' in flags:
        try:
            artist, song, quality = input_.split('-')
        except ValueError:
            if len(input_.split("-")) == 2:
                artist, song = input_.split('-')
                quality = d_quality
            else:
                await message.edit("WeW, Use that thing which is present on top floor of ur body 🌚")
                return

    if '-sdl' in flags:
        if 'track/' in input_link:
            await proper_trackdl(input_link, quality, message, loader, PATH, userge)
        elif 'album/' or 'playlist/' in input_link:
            await batch_dl(input_link, quality, message, loader, PATH, userge, to_zip)
    elif '-ddl' in flags:
        if 'track/' in input_link:
            await proper_trackdl(input_link, quality, message, loader, PATH, userge)
        elif 'album/' or 'playlist/' in input_link:
            await batch_dl(input_link, quality, message, loader, PATH, userge, to_zip)

    if '-dsong' in flags:
        await message.edit("Searching for Song 🔍")
        try:
            track = loader.download_name(
                artist=artist,
                song=song,
                output=PATH,
                quality=quality,
                recursive_quality=True,
                recursive_download=True,
                not_interface=True
            )
            await message.edit("Song found, Now Uploading 📤")
            await userge.send_audio(
                chat_id=message.chat.id,
                audio=track
            )
        except Exception:
            await message.edit("Song not Found 🚫")
    await message.delete()
    shutil.rmtree(PATH, ignore_errors=True)


async def proper_trackdl(link, qual, msg, client, dir_, u):
    if 'spotify' in link:
        await msg.edit("Trying to download song via Spotify Link 🥴")
        track = client.download_trackspo(
            link,
            output=dir_,
            quality=qual,
            recursive_quality=True,
            recursive_download=True,
            not_interface=True
        )
        await msg.edit("Now Uploading 📤")
        await u.send_audio(
            chat_id=msg.chat.id,
            audio=track
        )
    elif 'deezer' in link:
        await msg.edit("Trying to download song via Deezer Link 🥴")
        track = client.download_trackdee(
            link,
            output=dir_,
            quality=qual,
            recursive_quality=True,
            recursive_download=True,
            not_interface=True
        )
        await msg.edit("Now Uploading 📤")
        await u.send_audio(
            chat_id=msg.chat.id,
            audio=track
        )


async def batch_dl(link, qual, msg, client, dir_, u, allow_zip):
    if 'spotify' in link:
        if 'album/' in link:
            await msg.edit("Trying to download album 🤧")
            if allow_zip:
                _, zip_ = client.download_albumspo(
                    link,
                    output=dir_,
                    quality=qual,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                    zips=True
                )
                await msg.edit("Sending as Zip File 🗜")
                await u.send_document(
                    chat_id=msg.chat.id,
                    document=zip_
                )
            else:
                album_list = client.download_albumspo(
                    link,
                    output=dir_,
                    quality=qual,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                    zips=False)
                await msg.edit("Uploading Tracks 📤")
                for tracks in album_list:
                    await u.send_audio(
                        chat_id=msg.chat.id,
                        audio=tracks
                    )
        if 'playlist/' in link:
            await msg.edit("Trying to download Playlist 🎶")
            if allow_zip:
                _, zip_ = client.download_playlistspo(
                    link,
                    output=dir_,
                    quality=qual,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                    zips=True
                )
                await msg.edit("Sending as Zip 🗜")
                await u.send_document(
                    chat_id=msg.chat.id,
                    document=zip_
                )
            else:
                album_list = client.download_playlistspo(
                    link,
                    output=dir_,
                    quality=qual,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                    zips=False
                )
                await msg.edit("Uploading Tracks 📤")
                for tracks in album_list:
                    await u.send_audio(
                        chat_id=msg.chat.id,
                        audio=tracks
                    )

    if 'deezer' in link:
        if 'album/' in link:
            await msg.edit("Trying to download album 🤧")
            if allow_zip:
                _, zip_ = client.download_albumdee(
                    link,
                    output=dir_,
                    quality=qual,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                    zips=True
                )
                await msg.edit("Uploading as Zip File 🗜")
                await u.send_document(
                    chat_id=msg.chat.id,
                    document=zip_
                )
            else:
                album_list = client.download_albumdee(
                    link,
                    output=dir_,
                    quality=qual,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                    zips=False
                )
                await msg.edit("Uploading Tracks 📤")
                for tracks in album_list:
                    await u.send_audio(
                        chat_id=msg.chat.id,
                        audio=tracks
                    )
        elif 'playlist/' in link:
            await msg.edit("Trying to download Playlist 🎶")
            if allow_zip:
                _, zip_ = client.download_playlistdee(
                    link,
                    output=dir_,
                    quality=qual,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                    zips=True
                )
                await msg.edit("Sending as Zip File 🗜")
                await u.send_document(
                    chat_id=msg.chat.id,
                    document=zip_
                )
            else:
                album_list = client.download_playlistdee(
                    link,
                    output=dir_,
                    quality=qual,
                    recursive_quality=True,
                    recursive_download=True,
                    not_interface=True,
                    zips=False
                )
                await msg.edit("Uploading Tracks 📤")
                for tracks in album_list:
                    await u.send_audio(
                        chat_id=msg.chat.id,
                        audio=tracks
                    )
add_help_item(

"Download Songs/Albums/Playlists via "

                   "Sopitfy or Deezer Links. "

                   "\n**NOTE:** Music Quality is optional"
    )
