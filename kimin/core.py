from colorama import Fore, Back, Style
import datetime, asyncio, time, json
import psutil

class Get_Data:
	def __init__(kimin, mulai, sampai):
		kimin.mulai = mulai
		kimin.sampai = sampai
	
	@staticmethod
	def GetData(path="db/hasil.min"):
		with open(path) as dataku:
			data = dataku.read().splitlines()
		hasil = []
		for i in data:
			hasil.append(json.loads(i))
		return hasil
	
	@staticmethod
	def AddData(data, path='db/hasil.min'):
		with open(path,'a') as dataku:
			data=json.dumps(data)
			dataku.write(f"{data}\n")
		return "Tambah Data Complete"
	
	@staticmethod
	def GetCPU():
		hasil = psutil.cpu_percent(1)
		return f"{hasil} %"
	
	@staticmethod
	def GetRAM():
		hasil = psutil.virtual_memory()[2]
		return f"{hasil} %"
	
	@staticmethod
	def GetTime(format_data="%H:%M:%S"):
		now = datetime.datetime.now()
		now = now.strftime(format_data)
		return now

	@staticmethod
	def Before():
		now = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
		return now
	
	def GetURL(kimin, query, mode="populer"):
		query = query.replace(" ","%20").replace("@","%3A")
		if mode == "populer":
			url = f'https://twitter.com/search?q={query}%20until%3A{kimin.sampai}%20since%3A{kimin.mulai}&src=typed_query' 
		elif mode == "latest":
			url = f"https://twitter.com/search?q={query}%20until%3A{kimin.sampai}%20since%3A{kimin.mulai}&src=typed_query&f=live"
		elif mode == "people":
			url = f"https://twitter.com/search?q={query}%20until%3A{kimin.sampai}%20since%3A{kimin.mulai}&src=typed_query&f=user"
		elif mode == "foto":
			url = f'https://twitter.com/search?q={query}%20until%3A{kimin.sampai}%20since%3A{kimin.mulai}&src=typed_query&f=image'
		elif mode == 'vidio':
			url = f"https://twitter.com/search?q={query}%20until%3A{kimin.sampai}%20since%3A{kimin.mulai}&src=typed_query&f=video"
		return url

class Core:
	def __init__(kimin, page, url):
		kimin.wait = 0
		kimin.page = page
		kimin.url = url
	
	async def Speed_Test(kimin):
		start_time = time.time()
		await kimin.page.goto('https://www.youtube.com/')
		post = await kimin.page.query_selector_all('//div[@id="details"]')
		for data in post:
			judul = await data.query_selector('yt-formatted-string')
			link = await data.query_selector('a')
			# print({'Judul': await judul.inner_text(), 'Link': await link.get_attribute('href')})
		
		return time.time() - start_time
 
	async def Tunggu(kimin):
		await kimin.page.is_visible('//div[@data-testid="cellInnerDiv"]')
		await asyncio.sleep(kimin.wait)
	
	async def Waktu(kimin, elemen):
		hasil = await elemen.query_selector('time')
		if not hasil is None:
			hasil = await hasil.get_attribute('datetime')
		else:
			hasil = None
		return hasil
		
	async def Content(kimin, elemen):
		hasil = await elemen.query_selector('//div[@data-testid="tweetText"]')
		if not hasil is None:
			hasil = await hasil.inner_text()
		else:
			hasil = None
		return hasil
		
	async def Pengirim(kimin, elemen):
		hasil = await elemen.query_selector('a')
		if not hasil is None:
			hasil = await hasil.get_attribute('href')
		else:
			hasil = None
		return hasil
	
	async def Reply(kimin, elemen):
		hasil = await elemen.query_selector('//div[@data-testid="reply"]')
		if not hasil is None:
			hasil = await hasil.get_attribute('aria-label')
		else:
			hasil = None
		return hasil
	
	async def Retweet(kimin, elemen):
		hasil = await elemen.query_selector('//div[@data-testid="retweet"]')
		if not hasil is None:
			hasil = await hasil.get_attribute('aria-label')
		else:
			hasil = None
		return hasil
	
	async def Like(kimin, elemen):
		hasil = await elemen.query_selector('//div[@data-testid="like"]')
		if not hasil is None:
			hasil = await hasil.get_attribute('aria-label')
		else:
			hasil = None
		return hasil
	
	async def Penayangan(keys, elemen):
		hasil = await elemen.query_selector('//div[@class="css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1777fci r-bt1l66 r-1ny4l3l r-bztko3 r-lrvibr"]')
		hasil = await hasil.get_attribute('aria-label')
		return hasil
		
	async def Parser(kimin):
		hasil = []
		same = 0
		while True:
			pop_up = await kimin.page.locator('//div[@data-testid="sheetDialog"]').count()
			if pop_up > 0:
				print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.RED} Pop Up Notifikasi Terdeteksi!")
				await asyncio.sleep(1)
				print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.YELLOW} Menutup Pop Up Notifikasi!")
				await asyncio.sleep(1)
				try:
					pop = await kimin.page.click("text=Not now")
					print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.GREEN} Berhasil Menutup Pop Up Notifikasi!")
				
				except Exception as E:
					print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.RED} Gagal Menutup Pop Up Notifikasi!")
					await asyncio.sleep(1)
					print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.RED} Error : {Fore.WHITE} {E}")
					continue
			
			elemen = await kimin.page.query_selector_all('//article[@data-testid="tweet"]')
			if len(elemen) == 0 or same > 10:
				if len(elemen) == 0:
					print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.RED}Tidak Ada Data Postingan!")
				break
			
			print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.WHITE} {len(elemen)} {Fore.GREEN}Postingan Ditemukan!")
			await asyncio.sleep(1)
			print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.YELLOW} Parser {Fore.WHITE}{len(elemen)} {Fore.YELLOW} Data!")
			no = 1
			for data in elemen:
				try:
					pengirim = await kimin.Pengirim(data)
					content = await kimin.Content(data)
					waktu = await kimin.Waktu(data)
					reply = await kimin.Reply(data)
					retweet = await kimin.Retweet(data)
					like = await kimin.Like(data)
					# penayangan = await kimin.Penayangan(data)
					penayangan = None
					if pengirim is None or content is None or waktu is None or reply is None or retweet is None or like is None:
						print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.YELLOW} Parser Data No {Fore.WHITE}{no} {Fore.RED}ERROR!")
						no +=1
						continue
					temp = {
						"author": f"https://twitter.com{pengirim}", 
						"content":content,
						"datepost":waktu,
						"reply":reply,
						"retweet":retweet,
						"like":like,
						"penayangan":penayangan}
					if not temp in Get_Data.GetData():
						Get_Data.AddData(temp)
					print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.YELLOW} Parser Data No {Fore.WHITE}{no} {Fore.GREEN}DONE!")
				except Exception as e:
					print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.YELLOW} Parser Data No {Fore.WHITE}{no} {Fore.RED}ERROR!")
				no +=1
			
			pengirim = await kimin.Pengirim(elemen[len(elemen)-1])
			content = await kimin.Content(elemen[len(elemen)-1])
			waktu = await kimin.Waktu(elemen[len(elemen)-1])
			reply = await kimin.Reply(elemen[len(elemen)-1])
			retweet = await kimin.Retweet(elemen[len(elemen)-1])
			like = await kimin.Like(elemen[len(elemen)-1])
			penayangan = None
			temp = {
				"author": f"https://twitter.com{pengirim}", 
				"content":content,
				"datepost":waktu,
				"reply":reply,
				"retweet":retweet,
				"like":like,
				"penayangan":penayangan}
			if temp in Get_Data.GetData():
				same +=1
			else:
				same = 0
			print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.YELLOW} Scroll Down!")
			await asyncio.sleep(1)
			print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.GREEN} Scroll DONE!")
			await elemen[len(elemen)-1].scroll_into_view_if_needed()
		return hasil
		
	async def Pencarian(kimin):
		await kimin.page.goto(kimin.url)
		await kimin.Tunggu()
		kimin.page.set_default_timeout(timeout=30000)
		pop_up = await kimin.page.locator('//div[@data-testid="sheetDialog"]').count()
		if pop_up > 0:
			print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.RED} Pop Up Notifikasi Terdeteksi!")
			await asyncio.sleep(1)
			print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.YELLOW} Menutup Pop Up Notifikasi!")
			await asyncio.sleep(1)
			try:
				pop = await kimin.page.click("text=Not now")
				print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.GREEN} Berhasil Menutup Pop Up Notifikasi!")
			except Exception as E:
				print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.RED} Gagal Menutup Pop Up Notifikasi!")
				await asyncio.sleep(1)
				print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.RED} Error : {Fore.WHITE} {E}")
		hasil = await kimin.Parser()
		return hasil
			
	
		