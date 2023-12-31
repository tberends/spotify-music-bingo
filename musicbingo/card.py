import random

from slugify import slugify
from PIL import Image, ImageDraw, ImageFont


class MusicBingoCard:
    def __init__(self, title, playlist_tracks, player, game_id):
        self.title = title
        self.tracks = random.sample(playlist_tracks, 24)
        self.player = player
        self.game_id = game_id

    def get_filename(self):
        name = slugify(self.title)
        player = str(self.player).zfill(3)
        return "{}_{}_{}.png".format(self.game_id, name, player)

    def write(self):
        WIDTH = 1000
        HEIGHT = 1200

        BINGO_TITLE_Y = 60
        PLAYLIST_TITLE_Y = 20
        PLAYER_NAME_Y = 40

        CELL_WIDTH = 160
        CELL_HEIGHT = CELL_WIDTH
        CELL_PADDING = 5
        BOARD_X = 100
        BOARD_Y = 100

        img = Image.new("RGB", (WIDTH, HEIGHT), color=(255, 255, 255))
        d = ImageDraw.Draw(img)

        # BINGO Title
        fnt = ImageFont.truetype(
            ".\\layout\\ARLRDBD.TTF",
            60,
        )
        bingo_title_size = d.textsize("B   I   N   G   O", font=fnt)
        bingo_title_x = (WIDTH / 2) - (bingo_title_size[0] / 2)
        d.text(
            (bingo_title_x, BINGO_TITLE_Y),
            "B   I   N   G   O",
            font=fnt,
            fill=(0, 0, 0),
        )

        # Playlist Title
        fnt = ImageFont.truetype(
            ".\\layout\\ARLRDBD.TTF",
            40,
        )
        playlist_title_size = d.textsize(self.title, font=fnt)
        playlist_title_x = (WIDTH / 2) - (playlist_title_size[0] / 2)
        playlist_title_y = BINGO_TITLE_Y + PLAYLIST_TITLE_Y + bingo_title_size[1]
        d.text(
            (playlist_title_x, playlist_title_y), self.title, font=fnt, fill=(0, 0, 0)
        )

        # Player Name
        player_name = self.player.title()
        fnt = ImageFont.truetype(
            ".\\layout\\ARLRDBD.TTF",
            30,
        )
        player_name_size = d.textsize(player_name, font=fnt)
        player_name_x = (WIDTH / 2) - (player_name_size[0] / 2)
        player_name_y = (
            BINGO_TITLE_Y + PLAYLIST_TITLE_Y + PLAYER_NAME_Y + bingo_title_size[1]
        )
        d.text((player_name_x, player_name_y), player_name, font=fnt, fill=(0, 0, 0))

        # Add each of the bingo squares
        cells = self.tracks
        cells.insert(12, None)
        y1 = BOARD_Y
        fnt = ImageFont.truetype(
            ".\\layout\\ARLRDBD.TTF",
            20,
        )
        for idx, track in enumerate(cells):
            x1 = BOARD_X + ((idx % 5) * CELL_WIDTH)
            if idx % 5 == 0:
                y1 = y1 + CELL_HEIGHT

            x2 = x1 + CELL_WIDTH
            y2 = y1 + CELL_HEIGHT

            d.rectangle([(x1, y1), (x2, y2)], fill=(255, 255, 255), outline=(0, 0, 0))

            if track:
                title = "{} - {}".format(track["name"], track["artists"])
                wrapper = TextWrapper(title, fnt, CELL_WIDTH - (CELL_PADDING * 2))
                wrapped_text = wrapper.wrapped_text()

                # Get the width of the text
                text_width, _ = d.textsize(wrapped_text, font=fnt)

                # Calculate the x position to center the text
                text_x = (
                    x1
                    + CELL_PADDING
                    + ((CELL_WIDTH - (CELL_PADDING * 2) - text_width) / 2)
                )

                d.text(
                    (text_x, y1 + CELL_PADDING),
                    wrapped_text,
                    font=fnt,
                    fill=(0, 0, 0),
                )
            else:
                # put logo in the middle
                logo = Image.open(".\layout\\logo.jpg")
                logo = logo.resize((CELL_WIDTH, CELL_HEIGHT))
                img.paste(logo, (x1, y1))

                # img.save(self.get_filename())

        # Add a watermark footer link
        fnt = fnt = ImageFont.truetype(
            ".\layout\\ARLRDBD.TTF",
            16,
        )
        footer_y = BOARD_Y + (CELL_HEIGHT * 6) + 5
        d.text(
            (500, footer_y),
            "https://github.com/tberends/spotify-music-bingo",
            font=fnt,
            fill=(100, 100, 100),
        )

        img.save(self.get_filename())


# From: https://stackoverflow.com/a/49719319/990416
class TextWrapper(object):
    """Helper class to wrap text in lines, based on given text, font
    and max allowed line width.
    """

    def __init__(self, text, font, max_width):
        self.text = text
        self.text_lines = [
            " ".join([w.strip() for w in l.split(" ") if w])
            for l in text.split("\n")
            if l
        ]
        self.font = font
        self.max_width = max_width

        self.draw = ImageDraw.Draw(Image.new(mode="RGB", size=(100, 100)))

        self.space_width = self.draw.textsize(text=" ", font=self.font)[0]

    def get_text_width(self, text):
        return self.draw.textsize(text=text, font=self.font)[0]

    def wrapped_text(self):
        wrapped_lines = []
        buf = []
        buf_width = 0

        for line in self.text_lines:
            for word in line.split(" "):
                word_width = self.get_text_width(word)

                expected_width = (
                    word_width if not buf else buf_width + self.space_width + word_width
                )

                if expected_width <= self.max_width:
                    # word fits in line
                    buf_width = expected_width
                    buf.append(word)
                else:
                    # word doesn't fit in line
                    wrapped_lines.append(" ".join(buf))
                    buf = [word]
                    buf_width = word_width

            if buf:
                wrapped_lines.append(" ".join(buf))
                buf = []
                buf_width = 0

        return "\n".join(wrapped_lines)
