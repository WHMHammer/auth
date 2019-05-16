import flask

app = flask.Flask(__name__)


@app.route("/")
def index():
    return flask.render_template(
        "base.html",
        title="Home",
        content="""
            <h1>The Little Match Girl</h1>
                <p>It was so terribly cold. Snow was falling, and it was almost dark. Evening came on, the last evening of the year. In the cold and gloom a poor little girl, bareheaded and barefoot, was walking through the streets. Of course when she had left her house she'd had slippers on, but what good had they been? They were very big slippers, way too big for her, for they belonged to her mother. The little girl had lost them running across the road, where two carriages had rattled by terribly fast. One slipper she'd not been able to find again, and a boy had run off with the other, saying he could use it very well as a cradle some day when he had children of his own. And so the little girl walked on her naked feet, which were quite red and blue with the cold. In an old apron she carried several packages of matches, and she held a box of them in her hand. No one had bought any from her all day long, and no one had given her a cent.</p>
                <p>Shivering with cold and hunger, she crept along, a picture of misery, poor little girl! The snowflakes fell on her long fair hair, which hung in pretty curls over her neck. In all the windows lights were shining, and there was a wonderful smell of roast goose, for it was New Year's eve. Yes, she thought of that!</p>
                <p>In a corner formed by two houses, one of which projected farther out into the street than the other, she sat down and drew up her little feet under her. She was getting colder and colder, but did not dare to go home, for she had sold no matches, nor earned a single cent, and her father would surely beat her. Besides, it was cold at home, for they had nothing over them but a roof through which the wind whistled even though the biggest cracks had been stuffed with straw and rags.</p>
                <p>Her hands were almost dead with cold. Oh, how much one little match might warm her! If she could only take one from the box and rub it against the wall and warm her hands. She drew one out. R-r-ratch! How it sputtered and burned! It made a warm, bright flame, like a little candle, as she held her hands over it; but it gave a strange light! It really seemed to the little girl as if she were sitting before a great iron stove with shining brass knobs and a brass cover. How wonderfully the fire burned! How comfortable it was! The youngster stretched out her feet to warm them too; then the little flame went out, the stove vanished, and she had only the remains of the burnt match in her hand.</p>
                <p>She struck another match against the wall. It burned brightly, and when the light fell upon the wall it became transparent like a thin veil, and she could see through it into a room. On the table a snow-white cloth was spread, and on it stood a shining dinner service. The roast goose steamed gloriously, stuffed with apples and prunes. And what was still better, the goose jumped down from the dish and waddled along the floor with a knife and fork in its breast, right over to the little girl. Then the match went out, and she could see only the thick, cold wall. She lighted another match. Then she was sitting under the most beautiful Christmas tree. It was much larger and much more beautiful than the one she had seen last Christmas through the glass door at the rich merchant's home. Thousands of candles burned on the green branches, and colored pictures like those in the printshops looked down at her. The little girl reached both her hands toward them. Then the match went out. But the Christmas lights mounted higher. She saw them now as bright stars in the sky. One of them fell down, forming a long line of fire.</p>
                <p>"Now someone is dying," thought the little girl, for her old grandmother, the only person who had loved her, and who was now dead, had told her that when a star fell down a soul went up to God.</p>
                <p>She rubbed another match against the wall. It became bright again, and in the glow the old grandmother stood clear and shining, kind and lovely.</p>
                <p>"Grandmother!" cried the child. "Oh, take me with you! I know you will disappear when the match is burned out. You will vanish like the warm stove, the wonderful roast goose and the beautiful big Christmas tree!"</p>
                <p>And she quickly struck the whole bundle of matches, for she wished to keep her grandmother with her. And the matches burned with such a glow that it became brighter than daylight. Grandmother had never been so grand and beautiful. She took the little girl in her arms, and both of them flew in brightness and joy above the earth, very, very high, and up there was neither cold, nor hunger, nor fear-they were with God.</p>
                <p>But in the corner, leaning against the wall, sat the little girl with red cheeks and smiling mouth, frozen to death on the last evening of the old year. The New Year's sun rose upon a little pathetic figure. The child sat there, stiff and cold, holding the matches, of which one bundle was almost burned.</p>
                <p>"She wanted to warm herself," the people said. No one imagined what beautiful things she had seen, and how happily she had gone with her old grandmother into the bright New Year.</p>
        """,
        scripts=("js/index.js",)
    )

# register blueprint(s)
import auth
app.register_blueprint(auth.bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
