from discord_webhook import DiscordWebhook, DiscordEmbed

def send_webhook(webhook_url, nombre):

    webhook = DiscordWebhook(url=webhook_url, rate_limit_retry=True,content="@everyone",username="Crawler V2.0",avatar_url="https://www.vectorstock.com/royalty-free-vectors/crawler-vectors")

    embed = DiscordEmbed(title="Mise à jour du crawler ! ",description=f"Le nombre de pages trouvé {nombre}", color='03b2f8')
    webhook.add_embed(embed)


    webhook.execute()
