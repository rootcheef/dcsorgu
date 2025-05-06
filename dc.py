import discord
from discord import app_commands
from discord.ext import commands
import aiohttp

TOKEN = 'MTM2ODE1NTY5MzE3MjkyMDQwMA.G3-zX5.CdXGMc8PMrVpxUj8Ye8TsI8ed_VRNh4SjsXzPs'  # Bot token'ını buraya ekleyin
GUILD_ID = 1367462846505418804   # Sunucunun ID'si

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot giriş yaptı: {bot.user}")
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"✅ Slash komutları senkronize edildi: {len(synced)} komut")
    except Exception as e:
        print(f"❌ Komut senkronizasyon hatası: {e}")

# /sorgu komutu - Ad, Soyad ve İl ile sorgu yapar
@bot.tree.command(name="sorgu", description="Ad, soyad ve il ile sorgu yapar", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(ad="Ad girin", soyad="Soyad girin", il="İl girin")
async def sorgu(interaction: discord.Interaction, ad: str, soyad: str, il: str):
    await interaction.response.defer()

    url = f"https://api.sowixfree.xyz/sowixapi/adsoyadilce.php?ad={ad}&soyad={soyad}&il={il}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                await interaction.followup.send("❌ API bağlantı hatası!")
                return

            json_data = await resp.json()

    if json_data.get("success") and json_data.get("data"):
        for kişi in json_data["data"]:
            embed = discord.Embed(
                title="🩸 POLONYA SORGU SONUCU 🩸",
                description="🔍 **Aşağıda bulunan bilgiler sorgulama sonucudur.**",
                color=discord.Color.random()  # Her seferde farklı renk (gökkuşağı efekti)
            )

            embed.add_field(name="🧑 Ad Soyad", value=f"**{kişi['AD']} {kişi['SOYAD']}**", inline=True)
            embed.add_field(name="🆔 T.C. Kimlik", value=f"`{kişi['TC']}`", inline=True)
            embed.add_field(name="📅 Doğum Tarihi", value=kişi["DOGUMTARIHI"], inline=True)
            embed.add_field(name="🧬 Cinsiyet", value=kişi["CINSIYET"], inline=True)
            embed.add_field(name="🏡 Adres", value=f"📍 {kişi['ADRESIL']} / {kişi['ADRESILCE']}", inline=True)
            embed.add_field(name="👨‍👩‍👧 Anne - Baba", value=f"👩 {kişi['ANNEADI']}\n👨 {kişi['BABAADI']}", inline=True)
            embed.add_field(name="📍 Doğum Yeri", value=kişi["DOGUMYERI"], inline=True)
            embed.add_field(name="🗺️ Memleket", value=f"{kişi['MEMLEKETIL']} / {kişi['MEMLEKETILCE']}", inline=True)

            embed.set_image(url="https://i.ibb.co/s9KkfZvC/Adsz-tasarm.jpg")  # Geçerli bir resim linki
            embed.set_footer(text="🌐 Polonya Api Services • Devx:RootCheef", icon_url="https://i.ibb.co/s9KkfZvC/Adsz-tasarm.jpg")

            await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send("❗ Kişi bulunamadı.")

# /tcpro komutu - T.C. kimlik numarası ile sorgu yapar (Güncel API'ye göre)
@bot.tree.command(name="tcpro", description="T.C. kimlik numarası ile sorgu yapar", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(tc="T.C. Kimlik Numarası girin")
async def tcpro(interaction: discord.Interaction, tc: str):
    await interaction.response.defer()

    url = f"http://api.sowixfree.xyz/sowixapi/tc.php?tc={tc}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                await interaction.followup.send("❌ API bağlantı hatası!")
                return

            json_data = await resp.json()

    # Kontrol: 'data' anahtarı var mı ve boş mu değil mi?
    if json_data.get("success") and json_data.get("data"):
        try:
            kişi = json_data["data"]  # Tek bir kişi döndüğünü varsayıyoruz
            embed = discord.Embed(
                title="🩸 TC Pro Sorgu Sonucu 🩸",
                description="🔍 **Aşağıda bulunan bilgiler sorgulama sonucudur.**",
                color=discord.Color.random()
            )

            embed.add_field(name="🧑 Ad Soyad", value=f"**{kişi['AD']} {kişi['SOYAD']}**", inline=True)
            embed.add_field(name="🆔 T.C. Kimlik", value=f"`{kişi['TC']}`", inline=True)
            embed.add_field(name="👩‍👧 Anne Adı", value=kişi["ANNEADI"], inline=True)
            embed.add_field(name="🧑‍🦱 Baba Adı", value=kişi["BABAADI"], inline=True)
            embed.add_field(name="🗺️ Memleket", value=f"{kişi['MEMLEKETIL']} / {kişi['MEMLEKETILCE']}", inline=True)

            embed.set_image(url="https://i.ibb.co/s9KkfZvC/Adsz-tasarm.jpg")
            embed.set_footer(text="🌐 Polonya Api Services • Devx:RootCheef", icon_url="https://i.ibb.co/s9KkfZvC/Adsz-tasarm.jpg")

            await interaction.followup.send(embed=embed)
        except KeyError:
            await interaction.followup.send("❗ T.C. Kimlik numarasına ait bilgiler bulunamadı.")
    else:
        await interaction.followup.send("❗ API verisi boş ya da geçersiz.")

# /aile komutu - Aile bilgilerini sorgular
@bot.tree.command(name="aile", description="Aile bilgilerini sorgular", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(tc="T.C. Kimlik Numarası girin")
async def aile(interaction: discord.Interaction, tc: str):
    await interaction.response.defer()

    url = f"https://api.sowixfree.xyz/sowixapi/aile.php?tc={tc}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                await interaction.followup.send("❌ API bağlantı hatası!")
                return

            json_data = await resp.json()

    # Kontrol: 'data' anahtarı var mı ve boş mu değil mi?
    if json_data.get("success") and json_data.get("data"):
        for kişi in json_data["data"]:
            embed = discord.Embed(
                title="🩸 Aile Sorgu Sonucu 🩸",
                description="🔍 **Aşağıda bulunan aile bilgileri sorgulama sonucudur.**",
                color=discord.Color.random()
            )

            embed.add_field(name="🧑 Ad Soyad", value=f"**{kişi['AD']} {kişi['SOYAD']}**", inline=True)
            embed.add_field(name="🆔 T.C. Kimlik", value=f"`{kişi['TC']}`", inline=True)
            embed.add_field(name="📅 Doğum Tarihi", value=kişi["DOGUMTARIHI"], inline=True)
            embed.add_field(name="🧬 Cinsiyet", value=kişi["CINSIYET"], inline=True)
            embed.add_field(name="🏡 Adres", value=f"📍 {kişi['ADRESIL']} / {kişi['ADRESILCE']}", inline=True)
            embed.add_field(name="👨‍👩‍👧 Anne - Baba", value=f"👩 {kişi['ANNEADI']}\n👨 {kişi['BABAADI']}", inline=True)
            embed.add_field(name="📍 Doğum Yeri", value=kişi["DOGUMYERI"], inline=True)
            embed.add_field(name="🗺️ Memleket", value=f"{kişi['MEMLEKETIL']} / {kişi['MEMLEKETILCE']}", inline=True)

            embed.set_image(url="https://i.ibb.co/s9KkfZvC/Adsz-tasarm.jpg")
            embed.set_footer(text="🌐 Polonya Api Services • Devx:RootCheef", icon_url="https://i.ibb.co/s9KkfZvC/Adsz-tasarm.jpg")

            await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send("❗ Aile verisi boş ya da geçersiz.")

# /adres komutu - Adres bilgilerini sorgular
@bot.tree.command(name="adres", description="Adres bilgilerini sorgular", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(tc="T.C. Kimlik Numarası girin")
async def adres(interaction: discord.Interaction, tc: str):
    await interaction.response.defer()

    url = f"https://api.sowixfree.xyz/sowixapi/adres.php?tc={tc}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                await interaction.followup.send("❌ API bağlantı hatası!")
                return

            json_data = await resp.json()

    # Kontrol: 'data' anahtarı var mı ve boş mu değil mi?
    if json_data.get("success") and json_data.get("data"):
        try:
            kişi = json_data["data"]  # Tek bir kişi döndüğünü varsayıyoruz
            embed = discord.Embed(
                title="🩸 Adres Sorgu Sonucu 🩸",
                description="🔍 **Aşağıda bulunan adres bilgileri sorgulama sonucudur.**",
                color=discord.Color.random()
            )

            embed.add_field(name="🧑 Ad Soyad", value=f"**{kişi['AdSoyad']}**", inline=True)
            embed.add_field(name="🆔 T.C. Kimlik", value=f"`{kişi['KimlikNo']}`", inline=True)
            embed.add_field(name="📍 Doğum Yeri", value=kişi["DogumYeri"], inline=True)
            embed.add_field(name="🏠 İkametgah", value=kişi["Ikametgah"], inline=True)
            embed.add_field(name="💼 Vergi Numarası", value=kişi["VergiNumarasi"], inline=True)

            embed.set_image(url="https://i.ibb.co/s9KkfZvC/Adsz-tasarm.jpg")
            embed.set_footer(text="🌐 Polonya Api Services • Devx:RootCheef", icon_url="https://i.ibb.co/s9KkfZvC/Adsz-tasarm.jpg")

            await interaction.followup.send(embed=embed)
        except KeyError:
            await interaction.followup.send("❗ Adres bilgileri bulunamadı.")
    else:
        await interaction.followup.send("❗ API verisi boş ya da geçersiz.")

# /tcgsm komutu - T.C. kimlik numarası ile GSM numaralarını sorgular
@bot.tree.command(name="tcgsm", description="T.C. kimlik numarası ile GSM numaralarını sorgular", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(tc="T.C. Kimlik Numarası girin")
async def tcgsm(interaction: discord.Interaction, tc: str):
    await interaction.response.defer()

    url = f"http://api.sowixfree.xyz/sowixapi/tcgsm.php?tc={tc}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                await interaction.followup.send("❌ API bağlantı hatası!")
                return

            json_data = await resp.json()

    if json_data.get("success") and json_data.get("data"):
        embed = discord.Embed(
            title="📱 GSM Numarası Sorgu Sonucu 📱",
            description="🔍 **Aşağıda bulunan GSM numaraları sorgulama sonucudur.**",
            color=discord.Color.random()
        )
        
        # GSM numaralarını ekleyelim
        for kişi in json_data["data"]:
            embed.add_field(name="📞 GSM Numarası", value=f"`{kişi['GSM']}`", inline=True)

        embed.set_image(url="https://i.ibb.co/s9KkfZvC/Adsz-tasarm.jpg")
        embed.set_footer(text="🌐 Polonya Api Services • Devx:RootCheef", icon_url="https://i.ibb.co/s9KkfZvC/Adsz-tasarm.jpg")

        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send("❗ GSM numaraları bulunamadı.")

# /gsmtc komutu - GSM numarasına göre T.C. kimlik sorgular
@bot.tree.command(name="gsmtc", description="GSM numarasına göre T.C. kimlik sorgular", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(gsm="GSM Numarası girin")
async def gsmtc(interaction: discord.Interaction, gsm: str):
    await interaction.response.defer()

    url = f"http://api.sowixfree.xyz/sowixapi/gsm.php?gsm={gsm}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                await interaction.followup.send("❌ API bağlantı hatası!")
                return

            json_data = await resp.json()

    if json_data.get("success") and json_data.get("data"):
        kişi = json_data["data"]
        embed = discord.Embed(
            title="📱 GSM > TC Sorgu Sonucu 📱",
            description="🔍 **Aşağıda bulunan bilgiler sorgulama sonucudur.**",
            color=discord.Color.random()
        )

        embed.add_field(name="🆔 T.C. Kimlik", value=f"`{kişi['TC']}`", inline=True)
        embed.add_field(name="📞 GSM Numarası", value=f"`{kişi['GSM']}`", inline=True)

        embed.set_image(url="https://i.ibb.co/s9KkfZvC/Adsz-tasarm.jpg")
        embed.set_footer(text="🌐 Polonya Api Services • Devx:RootCheef", icon_url="https://i.ibb.co/s9KkfZvC/Adsz-tasarm.jpg")

        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send("❗ GSM numarasına ait T.C. Kimlik bulunamadı.")
        
# /gsmdetay komutu - GSM numarasına ait detayları sorgular
@bot.tree.command(name="gsmdetay", description="GSM numarasına ait detayları sorgular", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(gsm="GSM Numarası girin")
async def gsmdetay(interaction: discord.Interaction, gsm: str):
    await interaction.response.defer()

    url = f"http://api.sowixfree.xyz/sowixapi/gsmdetay.php?gsm={gsm}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                await interaction.followup.send("❌ API bağlantı hatası!")
                return

            json_data = await resp.json()

    # Kontrol: 'success' true ve 'Data' anahtarı mevcut mu?
    if json_data.get("success") and json_data.get("Data"):
        data = json_data["Data"]
        embed = discord.Embed(
            title="📱 GSM Detay Sorgu Sonucu 📱",
            description="🔍 **Aşağıda bulunan detaylar sorgulama sonucudur.**",
            color=discord.Color.random()
        )

        embed.add_field(name="🆔 T.C. Kimlik", value=f"`{data['TC']}`", inline=True)
        embed.add_field(name="🧑 Ad Soyad", value=f"**{data['AD']} {data['SOYAD']}**", inline=True)
        embed.add_field(name="📅 Doğum Tarihi", value=data["DOGUMTARIHI"], inline=True)
        embed.add_field(name="🏡 Adres", value=f"📍 {data['ADRESIL']} / {data['ADRESILCE']}", inline=True)
        embed.add_field(name="👩‍👧 Anne Adı", value=data["ANNEADI"], inline=True)
        embed.add_field(name="🧑‍🦱 Baba Adı", value=data["BABAADI"], inline=True)
        embed.add_field(name="🧬 Cinsiyet", value=data["CINSIYET"], inline=True)
        embed.add_field(name="💼 Vergi Numarası", value=data.get("VergiNumarasi", "Bilgi bulunamadı"), inline=True)
        embed.add_field(name="🏠 İkametgah", value=data.get("Ikametgah", "Bilgi bulunamadı"), inline=True)

        embed.set_image(url="https://i.ibb.co/s9KkfZvC/Adsz-tasarm.jpg")
        embed.set_footer(text="🌐 Polonya Api Services • Devx:RootCheef", icon_url="https://i.ibb.co/s9KkfZvC/Adsz-tasarm.jpg")

        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send("❗ GSM numarasına ait detaylar bulunamadı.")        
        
bot.run(TOKEN)
