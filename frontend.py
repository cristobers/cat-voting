import asyncio, aiohttp, json, sqlite3
from flask import Flask, render_template, request, make_response


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

def asyncio_get(url):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    a = loop.run_until_complete( fetch(url) )
    return a

@app.route("/")
def index():
    catimage = (asyncio_get('https://cataas.com/cat?json=true'))
    url = json.loads(catimage)
    print(url)
    catURL = f"https://cataas.com/cat/{url['_id']}"
    return render_template('index.html', catimagefinal=catURL)

@app.route("/vote-awesome", methods=["GET","POST"])
def awesomeVote():
    if request.method == "POST":
        conn = sqlite3.connect('cats.db')
        cur = conn.cursor()
        data = request.get_json()

        # if the cat doesnt exist, add the cat to the database and set its scores to 0
        res = cur.execute(f"SELECT URL FROM CATS WHERE URL = (?) ", (data['url'], ) )
        if res.fetchone() is None:
            data = (data['url'], 1, 0)
            cur.execute("""
                    INSERT OR IGNORE INTO CATS (URL, AWESOME, EXTRAAWESOME) VALUES (?,?,?)
                    """, data)
            conn.commit()
        else:
            # if the cat already exists, increment its vote by 1
            data = (data['url'], )  
            cur.execute("""
                        UPDATE CATS SET AWESOME = AWESOME + 1 WHERE URL = (?)
                        """, data)
            conn.commit()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route("/vote-extra-awesome", methods=["GET","POST"])
def extraAwesomeVote():
    if request.method == "POST":
        conn = sqlite3.connect('cats.db')
        cur = conn.cursor()
        data = request.get_json()

        # if the cat doesnt exist, add the cat to the database and set its scores to 0
        res = cur.execute(f"SELECT URL FROM CATS WHERE URL = (?) ", (data['url'], ) )
        if res.fetchone() is None:
            data = (data['url'], 0, 1)
            cur.execute("""
                    INSERT OR IGNORE INTO CATS (URL, AWESOME, EXTRAAWESOME) VALUES (?,?,?)
                    """, data)
            conn.commit()
        else:
            # if the cat already exists, increment its vote by 1
            data = (data['url'], )  
            cur.execute("""
                        UPDATE CATS SET EXTRAAWESOME = EXTRAAWESOME + 1 WHERE URL = (?)
                        """, data)
            conn.commit()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

if __name__ == '__main__':
    app.run(host='0.0.0.0', use_reloader=False)
