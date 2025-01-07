from flask import Flask, Response
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def gerar_feed_rss():
    # Configuração do feed
    url = "https://ge.globo.com/busca/?q=Vasco&order=recent&species=not%C3%ADcias"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Seletores CSS
    item_selector = "li.widget--card.widget--info"
    title_selector = "div.widget--info__title"
    url_selector = "a"

    # Gerar itens do feed
    rss_items = ""
    for item in soup.select(item_selector):
        title = item.select_one(title_selector).get_text(strip=True) if item.select_one(title_selector) else "Sem título"
        link = item.select_one(url_selector)['href'] if item.select_one(url_selector) else "#"
        rss_items += f"""
        <item>
          <title>{title}</title>
          <link>{link}</link>
          <pubDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}</pubDate>
        </item>
        """

    # Gerar RSS completo
    rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
      <channel>
        <title>Notícias do Vasco - ge.globo.com</title>
        <link>{url}</link>
        <description>Feed de notícias recentes do Vasco no site ge.globo.com</description>
        <language>pt-BR</language>
        <lastBuildDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}</lastBuildDate>
        {rss_items}
      </channel>
    </rss>
    """
    return Response(rss_feed, mimetype="application/rss+xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
