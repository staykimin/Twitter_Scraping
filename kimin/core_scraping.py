from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from colorama import Fore, Back, Style
from core import Get_Data
from core import Core
import asyncio, sys

import json, requests, subprocess
import argparse

async def Twitter(keyword, mulai, sampai, mode="populer"):
	async with async_playwright() as pw:
		mode = ['populer', 'latest', 'people', 'foto', 'vidio']
		with open("db/hasil.min",'w') as dataku:
			dataku.write("")
		browser = await pw.chromium.launch(headless=True)
		context = await browser.new_context()
		page = await context.new_page()
		print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.GREEN} Browser Berhasil Dibuka!")
		await asyncio.sleep(1)
		for i in mode:
			print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.YELLOW} Preparing Step!")
			
			sin = Get_Data(mulai, sampai)
			url = sin.GetURL(keyword, mode=i)
			
			cos = Core(page, url)
			await asyncio.sleep(1)
			print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.GREEN} Preparing Complete!")
			await asyncio.sleep(1)
			print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.YELLOW} Speed Testing!")
			await asyncio.sleep(1)
			speed = await cos.Speed_Test()
			print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.GREEN} Complete Speed Testing!")
			print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.GREEN} Kecepatan Browser : {Fore.LIGHTBLUE_EX}{speed} {Fore.WHITE}Detik!")
			await asyncio.sleep(1)
			print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.YELLOW} Menset Waktu Timeout!")
			cos.wait = speed+10
			await asyncio.sleep(1)
			print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.GREEN} Set Waktu Timeout Complete!")
			await asyncio.sleep(1)
			print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.YELLOW} Searching Step!")
			
			hasil = await cos.Pencarian()
			
			# x = input("Enter : ")
		print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.YELLOW} Menutup Browser!")
		await context.close()
		await browser.close()
		print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.GREEN} Berhasil Menutup Browser!")
	

parser = argparse.ArgumentParser()
parser.add_argument('--query', type=str, required=True)
parser.add_argument('--awal', type=str, required=True)
parser.add_argument('--akhir', type=str, required=True)

args  = parser.parse_args()
query = args.query.replace("_"," ")
mulai = args.awal
sampai= args.akhir

print(f"{Fore.WHITE}[#]{Fore.LIGHTBLUE_EX}[{Get_Data.GetTime()}] {Fore.WHITE}\t->{Fore.YELLOW} Membuka Browser")
asyncio.run(Twitter(query, mulai, sampai))
