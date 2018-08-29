#!/usr/local/bin/python3
from urllib.request import urlopen
from urllib.request import Request
import urllib.parse
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time
import random
#爬虫间隔秒数
sleepTimerMin = 5;
sleepTimerMax = 10;
#请求数据
def getData(pageIndex):
	url='http://www2.tjfdc.gov.cn/pages/efwgl2.aspx?id=gterqi_fwglspfxsxk'
	header={
	   'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
	}
	searchData={
		'__SPSCEditMenu': True,
		'MSOWebPartPage_PostbackSource': '',
		'MSOTlPn_SelectedWpId': '',
		'MSOTlPn_View': 0,
		'MSOTlPn_ShowSettings': False,
		'MSOGallery_SelectedLibrary': '',
		'MSOGallery_FilterString' : '',
		'MSOTlPn_Button': None,
		'__EVENTTARGET': 'ctl00%24ctl20%24g_010c6b5b_8f5c_4c45_b548_1a5f8e6e8b34%24ctl02',
		'__EVENTARGUMENT': '',
		'__REQUESTDIGEST': '0xCCE8E2D3994B0B06623478B58D73D65CFE5F49A41D36C8E6E6F92F4F1A88186FA2C15E36A44634181A10A4066CB7B0F5AE0B906AF39A2910D2B871C4284F54AF%2C09+Jul+2018+02%3A29%3A29+-0000',
		'MSOAuthoringConsole_FormContext': '',
		'MSOAC_EditDuringWorkflow': '',
		'MSOSPWebPartManager_DisplayModeName': 'Browse',
		'MSOWebPartPage_Shared': '',
		'MSOLayout_LayoutChanges': '',
		'MSOLayout_InDesignMode': '',
		'MSOSPWebPartManager_OldDisplayModeName': 'Browse',
		'MSOSPWebPartManager_StartWebPartEditingName': 'false',
		'__LASTFOCUS' : '',
		'__VIEWSTATE' : '%2FwEPDwUBMA9kFgJmD2QWAgIBD2QWBAIBD2QWAgILD2QWAmYPZBYCAgEPFgIeE1ByZXZpb3VzQ29udHJvbE1vZGULKYgBTWljcm9zb2Z0LlNoYXJlUG9pbnQuV2ViQ29udHJvbHMuU1BDb250cm9sTW9kZSwgTWljcm9zb2Z0LlNoYXJlUG9pbnQsIFZlcnNpb249MTIuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49NzFlOWJjZTExMWU5NDI5YwFkAgMPZBYIAgIPZBYCBSZnXzAxMGM2YjViXzhmNWNfNGM0NV9iNTQ4XzFhNWY4ZTZlOGIzNA9kFghmDw8WAh4HRW5hYmxlZGhkZAIBDw8WAh8BaGRkAgQPFCsADQ8WBh4LXyFEYXRhQm91bmRnHgtfIUl0ZW1Db3VudAKxUR4KU2hvd0hlYWRlcmhkZGQWCB4PSG9yaXpvbnRhbEFsaWduCyopU3lzdGVtLldlYi5VSS5XZWJDb250cm9scy5Ib3Jpem9udGFsQWxpZ24AHglGb250X0JvbGRoHglGb3JlQ29sb3IJAAAA%2Fx4EXyFTQgKEkARkZGRkZGRkFgQeCUdyaWRMaW5lcwsqI1N5c3RlbS5XZWIuVUkuV2ViQ29udHJvbHMuR3JpZExpbmVzAB8IAoCAIBQrAAMWCB4ETmFtZQUJbnZhcmNoYXIxHgpJc1JlYWRPbmx5aB4EVHlwZRkrAh4JRGF0YUZpZWxkBQludmFyY2hhcjEWCB8KBQVFeHByMR8LaB8MGSsCHw0FBUV4cHIxFggfCgUFRXhwcjIfC2gfDBkrAh8NBQVFeHByMhYCZg9kFjhmDw8WAh4HVmlzaWJsZWhkZAIBD2QWBmYPDxYIHgRUZXh0Be8BPGltZyBzcmM9Ii9fbGF5b3V0cy9pbWFnZXMvZ3VvdHVlcnFpL3Nob3V5ZS9ncmlkdmlld2Rhb2JpYW8uZ2lmIiAvPjxhIGhyZWY9Ii9wYWdlcy9kZXRhaWwuYXNweD9MaXN0SUQ9ZXJxaV94c3NwZnhremdzZ2cmYW1wO0l0ZW1JRD0xMDYzMCIgdGFyZ2V0PSJfYmxhbmsiIHN0eWxlPSJ0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHgiPua1t%2Ba4heWbrTHjgIExMS0xN%2BWPt%2BalvDwvYT4eBkhlaWdodBsAAAAAAAA5QAEAAAAeBVdpZHRoGwAAAAAAAHlAAQAAAB8IAoADFgIeBXN0eWxlBTtoZWlnaHQ6MjVweHRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweGQCAQ8PFgQfDwU8L3BhZ2VzL2RldGFpbC5hc3B4P0xpc3RJRD1lcnFpX3hzc3BmeGt6Z3NnZyZhbXA7SXRlbUlEPTEwNjMwHw5oFgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAgIPDxYCHw8FJea0peWbveWcn%2BaIv%2BWUruiuuOWtl1syMDE4XeesrDA0Njblj7cWAh8SBTtoZWlnaHQ6MjVweHRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweGQCAg9kFgZmDw8WCB8PBekBPGltZyBzcmM9Ii9fbGF5b3V0cy9pbWFnZXMvZ3VvdHVlcnFpL3Nob3V5ZS9ncmlkdmlld2Rhb2JpYW8uZ2lmIiAvPjxhIGhyZWY9Ii9wYWdlcy9kZXRhaWwuYXNweD9MaXN0SUQ9ZXJxaV94c3NwZnhremdzZ2cmYW1wO0l0ZW1JRD0xMDYyOSIgdGFyZ2V0PSJfYmxhbmsiIHN0eWxlPSJ0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHgiPumAuOajoOiLkTUtN%2BWPt%2BalvDwvYT4fEBsAAAAAAAA5QAEAAAAfERsAAAAAAAB5QAEAAAAfCAKAAxYCHxIFO2hlaWdodDoyNXB4dGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4ZAIBDw8WBB8PBTwvcGFnZXMvZGV0YWlsLmFzcHg%2FTGlzdElEPWVycWlfeHNzcGZ4a3pnc2dnJmFtcDtJdGVtSUQ9MTA2MjkfDmgWAh8SBTtoZWlnaHQ6MjVweHRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweGQCAg8PFgIfDwUl5rSl5Zu95Zyf5oi%2F5ZSu6K645a2XWzIwMThd56ysMDQ1NOWPtxYCHxIFO2hlaWdodDoyNXB4dGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4ZAIDD2QWBmYPDxYIHw8F6QE8aW1nIHNyYz0iL19sYXlvdXRzL2ltYWdlcy9ndW90dWVycWkvc2hvdXllL2dyaWR2aWV3ZGFvYmlhby5naWYiIC8%2BPGEgaHJlZj0iL3BhZ2VzL2RldGFpbC5hc3B4P0xpc3RJRD1lcnFpX3hzc3BmeGt6Z3NnZyZhbXA7SXRlbUlEPTEwNjI4IiB0YXJnZXQ9Il9ibGFuayIgc3R5bGU9InRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweCI%2B6YC45qOg6IuRMi005Y%2B35qW8PC9hPh8QGwAAAAAAADlAAQAAAB8RGwAAAAAAAHlAAQAAAB8IAoADFgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAgEPDxYEHw8FPC9wYWdlcy9kZXRhaWwuYXNweD9MaXN0SUQ9ZXJxaV94c3NwZnhremdzZ2cmYW1wO0l0ZW1JRD0xMDYyOB8OaBYCHxIFO2hlaWdodDoyNXB4dGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4ZAICDw8WAh8PBSXmtKXlm73lnJ%2FmiL%2FllK7orrjlrZdbMjAxOF3nrKwwNDUz5Y%2B3FgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAgQPZBYGZg8PFggfDwXoATxpbWcgc3JjPSIvX2xheW91dHMvaW1hZ2VzL2d1b3R1ZXJxaS9zaG91eWUvZ3JpZHZpZXdkYW9iaWFvLmdpZiIgLz48YSBocmVmPSIvcGFnZXMvZGV0YWlsLmFzcHg%2FTGlzdElEPWVycWlfeHNzcGZ4a3pnc2dnJmFtcDtJdGVtSUQ9MTA2MjciIHRhcmdldD0iX2JsYW5rIiBzdHlsZT0idGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4Ij7mgqbppqjoi5ExOeWPt%2BalvDwvYT4fEBsAAAAAAAA5QAEAAAAfERsAAAAAAAB5QAEAAAAfCAKAAxYCHxIFO2hlaWdodDoyNXB4dGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4ZAIBDw8WBB8PBTwvcGFnZXMvZGV0YWlsLmFzcHg%2FTGlzdElEPWVycWlfeHNzcGZ4a3pnc2dnJmFtcDtJdGVtSUQ9MTA2MjcfDmgWAh8SBTtoZWlnaHQ6MjVweHRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweGQCAg8PFgIfDwUl5rSl5Zu95Zyf5oi%2F5ZSu6K645a2XWzIwMThd56ysMDQ0OeWPtxYCHxIFO2hlaWdodDoyNXB4dGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4ZAIFD2QWBmYPDxYIHw8F6AE8aW1nIHNyYz0iL19sYXlvdXRzL2ltYWdlcy9ndW90dWVycWkvc2hvdXllL2dyaWR2aWV3ZGFvYmlhby5naWYiIC8%2BPGEgaHJlZj0iL3BhZ2VzL2RldGFpbC5hc3B4P0xpc3RJRD1lcnFpX3hzc3BmeGt6Z3NnZyZhbXA7SXRlbUlEPTEwNjI2IiB0YXJnZXQ9Il9ibGFuayIgc3R5bGU9InRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweCI%2B5oKm6aao6IuRMTjlj7fmpbw8L2E%2BHxAbAAAAAAAAOUABAAAAHxEbAAAAAAAAeUABAAAAHwgCgAMWAh8SBTtoZWlnaHQ6MjVweHRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweGQCAQ8PFgQfDwU8L3BhZ2VzL2RldGFpbC5hc3B4P0xpc3RJRD1lcnFpX3hzc3BmeGt6Z3NnZyZhbXA7SXRlbUlEPTEwNjI2Hw5oFgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAgIPDxYCHw8FJea0peWbveWcn%2BaIv%2BWUruiuuOWtl1syMDE4XeesrDA0NDjlj7cWAh8SBTtoZWlnaHQ6MjVweHRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweGQCBg9kFgZmDw8WCB8PBecBPGltZyBzcmM9Ii9fbGF5b3V0cy9pbWFnZXMvZ3VvdHVlcnFpL3Nob3V5ZS9ncmlkdmlld2Rhb2JpYW8uZ2lmIiAvPjxhIGhyZWY9Ii9wYWdlcy9kZXRhaWwuYXNweD9MaXN0SUQ9ZXJxaV94c3NwZnhremdzZ2cmYW1wO0l0ZW1JRD0xMDYyNSIgdGFyZ2V0PSJfYmxhbmsiIHN0eWxlPSJ0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHgiPuaCpummqOiLkTjlj7fmpbw8L2E%2BHxAbAAAAAAAAOUABAAAAHxEbAAAAAAAAeUABAAAAHwgCgAMWAh8SBTtoZWlnaHQ6MjVweHRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweGQCAQ8PFgQfDwU8L3BhZ2VzL2RldGFpbC5hc3B4P0xpc3RJRD1lcnFpX3hzc3BmeGt6Z3NnZyZhbXA7SXRlbUlEPTEwNjI1Hw5oFgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAgIPDxYCHw8FJea0peWbveWcn%2BaIv%2BWUruiuuOWtl1syMDE4XeesrDA0NDflj7cWAh8SBTtoZWlnaHQ6MjVweHRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweGQCBw9kFgZmDw8WCB8PBecBPGltZyBzcmM9Ii9fbGF5b3V0cy9pbWFnZXMvZ3VvdHVlcnFpL3Nob3V5ZS9ncmlkdmlld2Rhb2JpYW8uZ2lmIiAvPjxhIGhyZWY9Ii9wYWdlcy9kZXRhaWwuYXNweD9MaXN0SUQ9ZXJxaV94c3NwZnhremdzZ2cmYW1wO0l0ZW1JRD0xMDYyNCIgdGFyZ2V0PSJfYmxhbmsiIHN0eWxlPSJ0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHgiPuaCpummqOiLkTflj7fmpbw8L2E%2BHxAbAAAAAAAAOUABAAAAHxEbAAAAAAAAeUABAAAAHwgCgAMWAh8SBTtoZWlnaHQ6MjVweHRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweGQCAQ8PFgQfDwU8L3BhZ2VzL2RldGFpbC5hc3B4P0xpc3RJRD1lcnFpX3hzc3BmeGt6Z3NnZyZhbXA7SXRlbUlEPTEwNjI0Hw5oFgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAgIPDxYCHw8FJea0peWbveWcn%2BaIv%2BWUruiuuOWtl1syMDE4XeesrDA0NDblj7cWAh8SBTtoZWlnaHQ6MjVweHRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweGQCCA9kFgZmDw8WCB8PBecBPGltZyBzcmM9Ii9fbGF5b3V0cy9pbWFnZXMvZ3VvdHVlcnFpL3Nob3V5ZS9ncmlkdmlld2Rhb2JpYW8uZ2lmIiAvPjxhIGhyZWY9Ii9wYWdlcy9kZXRhaWwuYXNweD9MaXN0SUQ9ZXJxaV94c3NwZnhremdzZ2cmYW1wO0l0ZW1JRD0xMDYyMyIgdGFyZ2V0PSJfYmxhbmsiIHN0eWxlPSJ0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHgiPuaCpummqOiLkTblj7fmpbw8L2E%2BHxAbAAAAAAAAOUABAAAAHxEbAAAAAAAAeUABAAAAHwgCgAMWAh8SBTtoZWlnaHQ6MjVweHRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweGQCAQ8PFgQfDwU8L3BhZ2VzL2RldGFpbC5hc3B4P0xpc3RJRD1lcnFpX3hzc3BmeGt6Z3NnZyZhbXA7SXRlbUlEPTEwNjIzHw5oFgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAgIPDxYCHw8FJea0peWbveWcn%2BaIv%2BWUruiuuOWtl1syMDE4XeesrDA0NDXlj7cWAh8SBTtoZWlnaHQ6MjVweHRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweGQCCQ9kFgZmDw8WCB8PBecBPGltZyBzcmM9Ii9fbGF5b3V0cy9pbWFnZXMvZ3VvdHVlcnFpL3Nob3V5ZS9ncmlkdmlld2Rhb2JpYW8uZ2lmIiAvPjxhIGhyZWY9Ii9wYWdlcy9kZXRhaWwuYXNweD9MaXN0SUQ9ZXJxaV94c3NwZnhremdzZ2cmYW1wO0l0ZW1JRD0xMDYyMiIgdGFyZ2V0PSJfYmxhbmsiIHN0eWxlPSJ0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHgiPuaCpummqOiLkTXlj7fmpbw8L2E%2BHxAbAAAAAAAAOUABAAAAHxEbAAAAAAAAeUABAAAAHwgCgAMWAh8SBTtoZWlnaHQ6MjVweHRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweGQCAQ8PFgQfDwU8L3BhZ2VzL2RldGFpbC5hc3B4P0xpc3RJRD1lcnFpX3hzc3BmeGt6Z3NnZyZhbXA7SXRlbUlEPTEwNjIyHw5oFgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAgIPDxYCHw8FJea0peWbveWcn%2BaIv%2BWUruiuuOWtl1syMDE4XeesrDA0NDTlj7cWAh8SBTtoZWlnaHQ6MjVweHRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweGQCCg9kFgZmDw8WCB8PBegBPGltZyBzcmM9Ii9fbGF5b3V0cy9pbWFnZXMvZ3VvdHVlcnFpL3Nob3V5ZS9ncmlkdmlld2Rhb2JpYW8uZ2lmIiAvPjxhIGhyZWY9Ii9wYWdlcy9kZXRhaWwuYXNweD9MaXN0SUQ9ZXJxaV94c3NwZnhremdzZ2cmYW1wO0l0ZW1JRD0xMDYxNyIgdGFyZ2V0PSJfYmxhbmsiIHN0eWxlPSJ0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHgiPueip%2BW%2BoeWbrTI55Y%2B35qW8PC9hPh8QGwAAAAAAADlAAQAAAB8RGwAAAAAAAHlAAQAAAB8IAoADFgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAgEPDxYEHw8FPC9wYWdlcy9kZXRhaWwuYXNweD9MaXN0SUQ9ZXJxaV94c3NwZnhremdzZ2cmYW1wO0l0ZW1JRD0xMDYxNx8OaBYCHxIFO2hlaWdodDoyNXB4dGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4ZAICDw8WAh8PBSXmtKXlm73lnJ%2FmiL%2FllK7orrjlrZdbMjAxOF3nrKwwNDQy5Y%2B3FgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAgsPZBYGZg8PFggfDwXnATxpbWcgc3JjPSIvX2xheW91dHMvaW1hZ2VzL2d1b3R1ZXJxaS9zaG91eWUvZ3JpZHZpZXdkYW9iaWFvLmdpZiIgLz48YSBocmVmPSIvcGFnZXMvZGV0YWlsLmFzcHg%2FTGlzdElEPWVycWlfeHNzcGZ4a3pnc2dnJmFtcDtJdGVtSUQ9MTA2MTYiIHRhcmdldD0iX2JsYW5rIiBzdHlsZT0idGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4Ij7noqflvqHlm6005Y%2B35qW8PC9hPh8QGwAAAAAAADlAAQAAAB8RGwAAAAAAAHlAAQAAAB8IAoADFgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAgEPDxYEHw8FPC9wYWdlcy9kZXRhaWwuYXNweD9MaXN0SUQ9ZXJxaV94c3NwZnhremdzZ2cmYW1wO0l0ZW1JRD0xMDYxNh8OaBYCHxIFO2hlaWdodDoyNXB4dGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4ZAICDw8WAh8PBSXmtKXlm73lnJ%2FmiL%2FllK7orrjlrZdbMjAxOF3nrKwwNDQx5Y%2B3FgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAgwPZBYGZg8PFggfDwXnATxpbWcgc3JjPSIvX2xheW91dHMvaW1hZ2VzL2d1b3R1ZXJxaS9zaG91eWUvZ3JpZHZpZXdkYW9iaWFvLmdpZiIgLz48YSBocmVmPSIvcGFnZXMvZGV0YWlsLmFzcHg%2FTGlzdElEPWVycWlfeHNzcGZ4a3pnc2dnJmFtcDtJdGVtSUQ9MTA2MTUiIHRhcmdldD0iX2JsYW5rIiBzdHlsZT0idGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4Ij7noqflvqHlm60y5Y%2B35qW8PC9hPh8QGwAAAAAAADlAAQAAAB8RGwAAAAAAAHlAAQAAAB8IAoADFgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAgEPDxYEHw8FPC9wYWdlcy9kZXRhaWwuYXNweD9MaXN0SUQ9ZXJxaV94c3NwZnhremdzZ2cmYW1wO0l0ZW1JRD0xMDYxNR8OaBYCHxIFO2hlaWdodDoyNXB4dGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4ZAICDw8WAh8PBSXmtKXlm73lnJ%2FmiL%2FllK7orrjlrZdbMjAxOF3nrKwwNDQw5Y%2B3FgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAg0PZBYGZg8PFggfDwXnATxpbWcgc3JjPSIvX2xheW91dHMvaW1hZ2VzL2d1b3R1ZXJxaS9zaG91eWUvZ3JpZHZpZXdkYW9iaWFvLmdpZiIgLz48YSBocmVmPSIvcGFnZXMvZGV0YWlsLmFzcHg%2FTGlzdElEPWVycWlfeHNzcGZ4a3pnc2dnJmFtcDtJdGVtSUQ9MTA2MTQiIHRhcmdldD0iX2JsYW5rIiBzdHlsZT0idGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4Ij7noqflvqHlm60x5Y%2B35qW8PC9hPh8QGwAAAAAAADlAAQAAAB8RGwAAAAAAAHlAAQAAAB8IAoADFgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAgEPDxYEHw8FPC9wYWdlcy9kZXRhaWwuYXNweD9MaXN0SUQ9ZXJxaV94c3NwZnhremdzZ2cmYW1wO0l0ZW1JRD0xMDYxNB8OaBYCHxIFO2hlaWdodDoyNXB4dGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4ZAICDw8WAh8PBSXmtKXlm73lnJ%2FmiL%2FllK7orrjlrZdbMjAxOF3nrKwwNDM55Y%2B3FgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAg4PZBYGZg8PFggfDwXtATxpbWcgc3JjPSIvX2xheW91dHMvaW1hZ2VzL2d1b3R1ZXJxaS9zaG91eWUvZ3JpZHZpZXdkYW9iaWFvLmdpZiIgLz48YSBocmVmPSIvcGFnZXMvZGV0YWlsLmFzcHg%2FTGlzdElEPWVycWlfeHNzcGZ4a3pnc2dnJmFtcDtJdGVtSUQ9MTA2MTMiIHRhcmdldD0iX2JsYW5rIiBzdHlsZT0idGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4Ij7mvpzlkozmub4xNuOAgTE35Y%2B35qW8PC9hPh8QGwAAAAAAADlAAQAAAB8RGwAAAAAAAHlAAQAAAB8IAoADFgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAgEPDxYEHw8FPC9wYWdlcy9kZXRhaWwuYXNweD9MaXN0SUQ9ZXJxaV94c3NwZnhremdzZ2cmYW1wO0l0ZW1JRD0xMDYxMx8OaBYCHxIFO2hlaWdodDoyNXB4dGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4ZAICDw8WAh8PBSXmtKXlm73lnJ%2FmiL%2FllK7orrjlrZdbMjAxOF3nrKwwNDI25Y%2B3FgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAg8PZBYGZg8PFggfDwXtATxpbWcgc3JjPSIvX2xheW91dHMvaW1hZ2VzL2d1b3R1ZXJxaS9zaG91eWUvZ3JpZHZpZXdkYW9iaWFvLmdpZiIgLz48YSBocmVmPSIvcGFnZXMvZGV0YWlsLmFzcHg%2FTGlzdElEPWVycWlfeHNzcGZ4a3pnc2dnJmFtcDtJdGVtSUQ9MTA2MTIiIHRhcmdldD0iX2JsYW5rIiBzdHlsZT0idGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4Ij7mvpzlkozmub4xM%2BOAgTE05Y%2B35qW8PC9hPh8QGwAAAAAAADlAAQAAAB8RGwAAAAAAAHlAAQAAAB8IAoADFgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAgEPDxYEHw8FPC9wYWdlcy9kZXRhaWwuYXNweD9MaXN0SUQ9ZXJxaV94c3NwZnhremdzZ2cmYW1wO0l0ZW1JRD0xMDYxMh8OaBYCHxIFO2hlaWdodDoyNXB4dGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4ZAICDw8WAh8PBSXmtKXlm73lnJ%2FmiL%2FllK7orrjlrZdbMjAxOF3nrKwwNDI15Y%2B3FgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAhAPZBYGZg8PFggfDwXtATxpbWcgc3JjPSIvX2xheW91dHMvaW1hZ2VzL2d1b3R1ZXJxaS9zaG91eWUvZ3JpZHZpZXdkYW9iaWFvLmdpZiIgLz48YSBocmVmPSIvcGFnZXMvZGV0YWlsLmFzcHg%2FTGlzdElEPWVycWlfeHNzcGZ4a3pnc2dnJmFtcDtJdGVtSUQ9MTA2MTEiIHRhcmdldD0iX2JsYW5rIiBzdHlsZT0idGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4Ij7mvpzlkozmub4xMOOAgTE15Y%2B35qW8PC9hPh8QGwAAAAAAADlAAQAAAB8RGwAAAAAAAHlAAQAAAB8IAoADFgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAgEPDxYEHw8FPC9wYWdlcy9kZXRhaWwuYXNweD9MaXN0SUQ9ZXJxaV94c3NwZnhremdzZ2cmYW1wO0l0ZW1JRD0xMDYxMR8OaBYCHxIFO2hlaWdodDoyNXB4dGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4ZAICDw8WAh8PBSXmtKXlm73lnJ%2FmiL%2FllK7orrjlrZdbMjAxOF3nrKwwNDI05Y%2B3FgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAhEPZBYGZg8PFggfDwXgATxpbWcgc3JjPSIvX2xheW91dHMvaW1hZ2VzL2d1b3R1ZXJxaS9zaG91eWUvZ3JpZHZpZXdkYW9iaWFvLmdpZiIgLz48YSBocmVmPSIvcGFnZXMvZGV0YWlsLmFzcHg%2FTGlzdElEPWVycWlfeHNzcGZ4a3pnc2dnJmFtcDtJdGVtSUQ9MTA2MTAiIHRhcmdldD0iX2JsYW5rIiBzdHlsZT0idGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4Ij7lkIjlsYXlm608L2E%2BHxAbAAAAAAAAOUABAAAAHxEbAAAAAAAAeUABAAAAHwgCgAMWAh8SBTtoZWlnaHQ6MjVweHRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweGQCAQ8PFgQfDwU8L3BhZ2VzL2RldGFpbC5hc3B4P0xpc3RJRD1lcnFpX3hzc3BmeGt6Z3NnZyZhbXA7SXRlbUlEPTEwNjEwHw5oFgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAgIPDxYCHw8FJea0peWbveWcn%2BaIv%2BWUruiuuOWtl1syMDE4XeesrDA0MjPlj7cWAh8SBTtoZWlnaHQ6MjVweHRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweGQCEg9kFgZmDw8WCB8PBeABPGltZyBzcmM9Ii9fbGF5b3V0cy9pbWFnZXMvZ3VvdHVlcnFpL3Nob3V5ZS9ncmlkdmlld2Rhb2JpYW8uZ2lmIiAvPjxhIGhyZWY9Ii9wYWdlcy9kZXRhaWwuYXNweD9MaXN0SUQ9ZXJxaV94c3NwZnhremdzZ2cmYW1wO0l0ZW1JRD0xMDYwOSIgdGFyZ2V0PSJfYmxhbmsiIHN0eWxlPSJ0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHgiPuWQiOWxheWbrTwvYT4fEBsAAAAAAAA5QAEAAAAfERsAAAAAAAB5QAEAAAAfCAKAAxYCHxIFO2hlaWdodDoyNXB4dGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4ZAIBDw8WBB8PBTwvcGFnZXMvZGV0YWlsLmFzcHg%2FTGlzdElEPWVycWlfeHNzcGZ4a3pnc2dnJmFtcDtJdGVtSUQ9MTA2MDkfDmgWAh8SBTtoZWlnaHQ6MjVweHRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweGQCAg8PFgIfDwUl5rSl5Zu95Zyf5oi%2F5ZSu6K645a2XWzIwMThd56ysMDQyMuWPtxYCHxIFO2hlaWdodDoyNXB4dGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4ZAITD2QWBmYPDxYIHw8F4wE8aW1nIHNyYz0iL19sYXlvdXRzL2ltYWdlcy9ndW90dWVycWkvc2hvdXllL2dyaWR2aWV3ZGFvYmlhby5naWYiIC8%2BPGEgaHJlZj0iL3BhZ2VzL2RldGFpbC5hc3B4P0xpc3RJRD1lcnFpX3hzc3BmeGt6Z3NnZyZhbXA7SXRlbUlEPTEwNjA4IiB0YXJnZXQ9Il9ibGFuayIgc3R5bGU9InRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweCI%2B5pel6L6J6ZuF6IuRPC9hPh8QGwAAAAAAADlAAQAAAB8RGwAAAAAAAHlAAQAAAB8IAoADFgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAgEPDxYEHw8FPC9wYWdlcy9kZXRhaWwuYXNweD9MaXN0SUQ9ZXJxaV94c3NwZnhremdzZ2cmYW1wO0l0ZW1JRD0xMDYwOB8OaBYCHxIFO2hlaWdodDoyNXB4dGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4ZAICDw8WAh8PBSXmtKXlm73lnJ%2FmiL%2FllK7orrjlrZdbMjAxOF3nrKwwNDIx5Y%2B3FgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAhQPZBYGZg8PFggfDwXjATxpbWcgc3JjPSIvX2xheW91dHMvaW1hZ2VzL2d1b3R1ZXJxaS9zaG91eWUvZ3JpZHZpZXdkYW9iaWFvLmdpZiIgLz48YSBocmVmPSIvcGFnZXMvZGV0YWlsLmFzcHg%2FTGlzdElEPWVycWlfeHNzcGZ4a3pnc2dnJmFtcDtJdGVtSUQ9MTA2MDciIHRhcmdldD0iX2JsYW5rIiBzdHlsZT0idGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4Ij7ml6Xovonpm4Xoi5E8L2E%2BHxAbAAAAAAAAOUABAAAAHxEbAAAAAAAAeUABAAAAHwgCgAMWAh8SBTtoZWlnaHQ6MjVweHRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweGQCAQ8PFgQfDwU8L3BhZ2VzL2RldGFpbC5hc3B4P0xpc3RJRD1lcnFpX3hzc3BmeGt6Z3NnZyZhbXA7SXRlbUlEPTEwNjA3Hw5oFgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAgIPDxYCHw8FJea0peWbveWcn%2BaIv%2BWUruiuuOWtl1syMDE4XeesrDA0MjDlj7cWAh8SBTtoZWlnaHQ6MjVweHRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweGQCFQ9kFgZmDw8WCB8PBeABPGltZyBzcmM9Ii9fbGF5b3V0cy9pbWFnZXMvZ3VvdHVlcnFpL3Nob3V5ZS9ncmlkdmlld2Rhb2JpYW8uZ2lmIiAvPjxhIGhyZWY9Ii9wYWdlcy9kZXRhaWwuYXNweD9MaXN0SUQ9ZXJxaV94c3NwZnhremdzZ2cmYW1wO0l0ZW1JRD0xMDYwNiIgdGFyZ2V0PSJfYmxhbmsiIHN0eWxlPSJ0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHgiPuaPveaZr%2Bi9qTwvYT4fEBsAAAAAAAA5QAEAAAAfERsAAAAAAAB5QAEAAAAfCAKAAxYCHxIFO2hlaWdodDoyNXB4dGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4ZAIBDw8WBB8PBTwvcGFnZXMvZGV0YWlsLmFzcHg%2FTGlzdElEPWVycWlfeHNzcGZ4a3pnc2dnJmFtcDtJdGVtSUQ9MTA2MDYfDmgWAh8SBTtoZWlnaHQ6MjVweHRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweGQCAg8PFgIfDwUl5rSl5Zu95Zyf5oi%2F5ZSu6K645a2XWzIwMThd56ysMDQxOeWPtxYCHxIFO2hlaWdodDoyNXB4dGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4ZAIWD2QWBmYPDxYIHw8F4AE8aW1nIHNyYz0iL19sYXlvdXRzL2ltYWdlcy9ndW90dWVycWkvc2hvdXllL2dyaWR2aWV3ZGFvYmlhby5naWYiIC8%2BPGEgaHJlZj0iL3BhZ2VzL2RldGFpbC5hc3B4P0xpc3RJRD1lcnFpX3hzc3BmeGt6Z3NnZyZhbXA7SXRlbUlEPTEwNjA1IiB0YXJnZXQ9Il9ibGFuayIgc3R5bGU9InRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweCI%2B5o%2B95pmv6L2pPC9hPh8QGwAAAAAAADlAAQAAAB8RGwAAAAAAAHlAAQAAAB8IAoADFgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAgEPDxYEHw8FPC9wYWdlcy9kZXRhaWwuYXNweD9MaXN0SUQ9ZXJxaV94c3NwZnhremdzZ2cmYW1wO0l0ZW1JRD0xMDYwNR8OaBYCHxIFO2hlaWdodDoyNXB4dGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4ZAICDw8WAh8PBSXmtKXlm73lnJ%2FmiL%2FllK7orrjlrZdbMjAxOF3nrKwwNDE45Y%2B3FgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAhcPZBYGZg8PFggfDwXgATxpbWcgc3JjPSIvX2xheW91dHMvaW1hZ2VzL2d1b3R1ZXJxaS9zaG91eWUvZ3JpZHZpZXdkYW9iaWFvLmdpZiIgLz48YSBocmVmPSIvcGFnZXMvZGV0YWlsLmFzcHg%2FTGlzdElEPWVycWlfeHNzcGZ4a3pnc2dnJmFtcDtJdGVtSUQ9MTA2MDQiIHRhcmdldD0iX2JsYW5rIiBzdHlsZT0idGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4Ij7nv6DmqL7lm608L2E%2BHxAbAAAAAAAAOUABAAAAHxEbAAAAAAAAeUABAAAAHwgCgAMWAh8SBTtoZWlnaHQ6MjVweHRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweGQCAQ8PFgQfDwU8L3BhZ2VzL2RldGFpbC5hc3B4P0xpc3RJRD1lcnFpX3hzc3BmeGt6Z3NnZyZhbXA7SXRlbUlEPTEwNjA0Hw5oFgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAgIPDxYCHw8FJea0peWbveWcn%2BaIv%2BWUruiuuOWtl1syMDE4XeesrDA0MTflj7cWAh8SBTtoZWlnaHQ6MjVweHRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweGQCGA9kFgZmDw8WCB8PBeABPGltZyBzcmM9Ii9fbGF5b3V0cy9pbWFnZXMvZ3VvdHVlcnFpL3Nob3V5ZS9ncmlkdmlld2Rhb2JpYW8uZ2lmIiAvPjxhIGhyZWY9Ii9wYWdlcy9kZXRhaWwuYXNweD9MaXN0SUQ9ZXJxaV94c3NwZnhremdzZ2cmYW1wO0l0ZW1JRD0xMDYwMyIgdGFyZ2V0PSJfYmxhbmsiIHN0eWxlPSJ0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHgiPua7n%2Ba5luiLkTwvYT4fEBsAAAAAAAA5QAEAAAAfERsAAAAAAAB5QAEAAAAfCAKAAxYCHxIFO2hlaWdodDoyNXB4dGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4ZAIBDw8WBB8PBTwvcGFnZXMvZGV0YWlsLmFzcHg%2FTGlzdElEPWVycWlfeHNzcGZ4a3pnc2dnJmFtcDtJdGVtSUQ9MTA2MDMfDmgWAh8SBTtoZWlnaHQ6MjVweHRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweGQCAg8PFgIfDwUl5rSl5Zu95Zyf5oi%2F5ZSu6K645a2XWzIwMThd56ysMDQxNuWPtxYCHxIFO2hlaWdodDoyNXB4dGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4ZAIZD2QWBmYPDxYIHw8F4wE8aW1nIHNyYz0iL19sYXlvdXRzL2ltYWdlcy9ndW90dWVycWkvc2hvdXllL2dyaWR2aWV3ZGFvYmlhby5naWYiIC8%2BPGEgaHJlZj0iL3BhZ2VzL2RldGFpbC5hc3B4P0xpc3RJRD1lcnFpX3hzc3BmeGt6Z3NnZyZhbXA7SXRlbUlEPTEwNjAyIiB0YXJnZXQ9Il9ibGFuayIgc3R5bGU9InRleHQtZGVjb3JhdGlvbjpub25lOyBjb2xvcjpibGFjaztmb250LXNpemU6MTRweCI%2B57Sr5LmQ5r6c5bqtPC9hPh8QGwAAAAAAADlAAQAAAB8RGwAAAAAAAHlAAQAAAB8IAoADFgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAgEPDxYEHw8FPC9wYWdlcy9kZXRhaWwuYXNweD9MaXN0SUQ9ZXJxaV94c3NwZnhremdzZ2cmYW1wO0l0ZW1JRD0xMDYwMh8OaBYCHxIFO2hlaWdodDoyNXB4dGV4dC1kZWNvcmF0aW9uOm5vbmU7IGNvbG9yOmJsYWNrO2ZvbnQtc2l6ZToxNHB4ZAICDw8WAh8PBSXmtKXlm73lnJ%2FmiL%2FllK7orrjlrZdbMjAxOF3nrKwwNDE15Y%2B3FgIfEgU7aGVpZ2h0OjI1cHh0ZXh0LWRlY29yYXRpb246bm9uZTsgY29sb3I6YmxhY2s7Zm9udC1zaXplOjE0cHhkAhoPDxYCHw5oZGQCGw8PFgIfDmhkZAIFDxBkZBYBZmQCCg9kFgICAw9kFgICAQ8PFgIfDmdkFgQCAQ8PFgIfDmhkFhwCAQ8PFgIfDmhkZAIDDxYCHw5oZAIFDw8WAh8OaGRkAgcPFgIfDmhkAgkPDxYCHw5oZGQCCw8PFgIfDmhkZAINDw8WAh8OaGRkAg8PDxYEHwFoHw5oZGQCEQ8PFgIfDmhkZAITDw8WBB8BaB8OaGRkAhUPDxYCHw5oZGQCFw8WAh8OaGQCGQ8WAh8OaGQCGw8PFgIfDmdkZAIDDw8WAh8OZ2QWBgIBDw8WAh8OZ2RkAgMPDxYGHhhwZXJzaXN0ZWRFcnJvckFjdGlvblRyZWVkHhtwZXJzaXN0ZWRFcnJvckFjdGlvblRyZWVJZHNkHw5nZGQCBQ8PFgIfDmdkZAIQD2QWAmYPD2QWAh4FY2xhc3MFGG1zLXNidGFibGUgbXMtc2J0YWJsZS1leGQCEg9kFioCAw9kFgJmDw8WAh8OaGRkAgUPZBYCZg8PFgIfDmhkZAIHD2QWAmYPDxYCHw5oZGQCCQ9kFgJmDw8WAh8OaGRkAgsPZBYCZg8PFgIfDmhkZAIND2QWAmYPDxYCHw5oZGQCDw9kFgJmDw8WAh8OaGRkAhEPZBYCZg8PFgIfDmhkZAITD2QWAmYPDxYCHw5oZGQCFQ9kFgJmDw8WAh8OaGRkAhcPZBYCZg8PFgIfDmhkZAIZD2QWAmYPDxYCHw5oZGQCGw9kFgJmDw8WAh8OaGRkAh0PZBYCZg8PFgIfDmhkZAIfD2QWAmYPDxYCHw5oZGQCIQ9kFgJmDw8WAh8OaGRkAiMPZBYCZg8PFgIfDmhkZAIlD2QWAmYPDxYCHw5oZGQCJw9kFgJmDw8WAh8OaGRkAikPZBYCZg8PFgIfDmhkZAIrD2QWAmYPDxYCHw5oZGQYAQVCY3RsMDAkY3RsMjAkZ18wMTBjNmI1Yl84ZjVjXzRjNDVfYjU0OF8xYTVmOGU2ZThiMzQkR3JpZFZpZXdXZWJQYXJ0DzwrAAoBCAKhA2S%2BcOUfpOrS%2BLg%2F2aspRUad6l1oYg%3D%3D',
		'__EVENTVALIDATION': '%2FwEWpgMC0fDY0QgCxInAwAkCqMLM5gsCqMLgwQQC45a9qAgC8%2FmXxgQC7PmXxgQC7fmXxgQC7vmXxgQC7%2FmXxgQC6PmXxgQC6fmXxgQC6vmXxgQC%2B%2FmXxgQC9PmXxgQC7PnXxQQC7PnbxQQC7PnfxQQC7PnjxQQC7PnnxQQC7PnrxQQC7PnvxQQC7PnzxQQC7Pm3xgQC7Pm7xgQC7fnXxQQC7fnbxQQC7fnfxQQC7fnjxQQC7fnnxQQC7fnrxQQC7fnvxQQC7fnzxQQC7fm3xgQC7fm7xgQC7vnXxQQC7vnbxQQC7vnfxQQC7vnjxQQC7vnnxQQC7vnrxQQC7vnvxQQC7vnzxQQC7vm3xgQC7vm7xgQC7%2FnXxQQC7%2FnbxQQC7%2FnfxQQC7%2FnjxQQC7%2FnnxQQC7%2FnrxQQC7%2FnvxQQC7%2FnzxQQC7%2Fm3xgQC7%2Fm7xgQC6PnXxQQC6PnbxQQC6PnfxQQC6PnjxQQC6PnnxQQC6PnrxQQC6PnvxQQC6PnzxQQC6Pm3xgQC6Pm7xgQC6fnXxQQC6fnbxQQC6fnfxQQC6fnjxQQC6fnnxQQC6fnrxQQC6fnvxQQC6fnzxQQC6fm3xgQC6fm7xgQC6vnXxQQC6vnbxQQC6vnfxQQC6vnjxQQC6vnnxQQC6vnrxQQC6vnvxQQC6vnzxQQC6vm3xgQC6vm7xgQC%2B%2FnXxQQC%2B%2FnbxQQC%2B%2FnfxQQC%2B%2FnjxQQC%2B%2FnnxQQC%2B%2FnrxQQC%2B%2FnvxQQC%2B%2FnzxQQC%2B%2Fm3xgQC%2B%2Fm7xgQC9PnXxQQC9PnbxQQC9PnfxQQC9PnjxQQC9PnnxQQC9PnrxQQC9PnvxQQC9PnzxQQC9Pm3xgQC9Pm7xgQCyriwkgMCp4GW5w0CvJb0zAcCmf%2Fb0QEC9sW5pwwC06qfjAYCqLP9EQKFmOPmCgKy8qO4AgKP24GNDALKuLSSAwKngZrnDQK8lvjMBwKZ%2F9%2FRAQL2xb2nDALTqqOMBgKos4ERAoWY5%2BYKArLyp7gCAo%2FbhY0MAsq4uJIDAqeBnucNAryW%2FMwHApn%2F49EBAvbFwaYMAtOqp4wGAqizhREChZjr5goCsvKruAICj9uJjQwCyri8kgMCp4Gi5w0CvJaAzAcCmf%2Fn0QEC9sXFpgwC06qrjAYCqLOJEQKFmO%2FmCgKy8q%2B4AgKP242NDALKuMCRAwKngabnDQK8loTMBwKZ%2F%2BvRAQL2xcmmDALTqq%2BMBgKos40RAoWY8%2BYKArLys7gCAo%2FbkY0MAsq4xJEDAqeBqucNAryWiMwHApn%2F79EBAvbFzaYMAtOqs4wGAqizkREChZj35goCsvK3uAICj9uVjQwCyrjIkQMCp4Gu5w0CvJaMzAcCmf%2Fz0QEC9sXRpgwC06q3jAYCqLOVEQKFmPvmCgKy8ru4AgKP25mNDALKuMyRAwKngbLnDQK8lpDMBwKZ%2F%2FfRAQL2xdWmDALTqruMBgKos5kRAoWY%2F%2BYKArLyv7gCAo%2FbnY0MAsq4kJIDAqeB9ucNAryW1MwHApn%2Fu9IBAvbFmacMAtOq%2F4wGAqiz3REChZjD5goCsvKDuAICj9vhjQwCyriUkgMCp4H65w0CvJbYzAcCmf%2B%2F0gEC9sWdpwwC06qDjAYCqLPhEQKFmMfmCgKy8oe4AgKP2%2BWNDALLuLCSAwKggZbnDQK9lvTMBwKa%2F9vRAQL3xbmnDALMqp%2BMBgKps%2F0RAoaY4%2BYKArPyo7gCAojbgY0MAsu4tJIDAqCBmucNAr2W%2BMwHApr%2F39EBAvfFvacMAsyqo4wGAqmzgREChpjn5goCs%2FKnuAICiNuFjQwCy7i4kgMCoIGe5w0CvZb8zAcCmv%2Fj0QEC98XBpgwCzKqnjAYCqbOFEQKGmOvmCgKz8qu4AgKI24mNDALLuLySAwKggaLnDQK9loDMBwKa%2F%2BfRAQL3xcWmDALMqquMBgKps4kRAoaY7%2BYKArPyr7gCAojbjY0MAsu4wJEDAqCBpucNAr2WhMwHApr%2F69EBAvfFyaYMAsyqr4wGAqmzjREChpjz5goCs%2FKzuAICiNuRjQwCy7jEkQMCoIGq5w0CvZaIzAcCmv%2Fv0QEC98XNpgwCzKqzjAYCqbOREQKGmPfmCgKz8re4AgKI25WNDALLuMiRAwKgga7nDQK9lozMBwKa%2F%2FPRAQL3xdGmDALMqreMBgKps5URAoaY%2B%2BYKArPyu7gCAojbmY0MAsu4zJEDAqCBsucNAr2WkMwHApr%2F99EBAvfF1aYMAsyqu4wGAqmzmREChpj%2F5goCs%2FK%2FuAICiNudjQwCy7iQkgMCoIH25w0CvZbUzAcCmv%2B70gEC98WZpwwCzKr%2FjAYCqbPdEQKGmMPmCgKz8oO4AgKI2%2BGNDALLuJSSAwKggfrnDQK9ltjMBwKa%2F7%2FSAQL3xZ2nDALMqoOMBgKps%2BERAoaYx%2BYKArPyh7gCAojb5Y0MAsS4sJIDAqGBlucNAr6W9MwHApv%2F29EBAvDFuacMAs2qn4wGAqqz%2FRECh5jj5goCrPKjuAICiduBjQwCxLi0kgMCoYGa5w0Cvpb4zAcCm%2F%2Ff0QEC8MW9pwwCzaqjjAYCqrOBEQKHmOfmCgKs8qe4AgKJ24WNDALEuLiSAwKhgZ7nDQK%2BlvzMBwKb%2F%2BPRAQLwxcGmDALNqqeMBgKqs4URAoeY6%2BYKAqzyq7gCAonbiY0MAsS4vJIDAqGBoucNAr6WgMwHApv%2F59EBAvDFxaYMAs2qq4wGAqqziRECh5jv5goCrPKvuAICiduNjQwCxLjAkQMCoYGm5w0CvpaEzAcCm%2F%2Fr0QEC8MXJpgwCzaqvjAYCqrONEQKHmPPmCgKs8rO4AgKJ25GNDALEuMSRAwKhgarnDQK%2BlojMBwKb%2F%2B%2FRAQLwxc2mDALNqrOMBgKqs5ERAoeY9%2BYKAqzyt7gCAonblY0MAsS4yJEDAqGBrucNAr6WjMwHApv%2F89EBAvDF0aYMAs2qt4wGAqqzlRECh5j75goCrPK7uAICiduZjQwCxLjMkQMCoYGy5w0CvpaQzAcCm%2F%2F30QEC8MXVpgwCzaq7jAYCqrOZEQKHmP%2FmCgKs8r%2B4AgKJ252NDALEuJCSAwKhgfbnDQK%2BltTMBwKb%2F7vSAQLwxZmnDALNqv%2BMBgKqs90RAoeYw%2BYKAqzyg7gCAonb4Y0MAsS4lJIDAqGB%2BucNAr6W2MwHApv%2Fv9IBAvDFnacMAs2qg4wGAqqz4RECh5jH5goCrPKHuAICidvljQwCxbiwkgMCooGW5w0Cv5b0zAcClP%2Fb0QEC8cW5pwwCzqqfjAYCq7P9EQKAmOPmCgKt8qO4AgKK24GNDALFuLSSAwKigZrnDQK%2FlvjMBwKU%2F9%2FRAQLxxb2nDALOqqOMBgKrs4ERh1KI9LTG82Q7UKaueMh%2BNFAci7U%3D',
		'ctl00%24g_df89adf4_0e73_48b4_813d_57d85e6663cb%24S275DD2BF_InputKeywords': '', 
		'ctl00$ctl20$g_010c6b5b_8f5c_4c45_b548_1a5f8e6e8b34$wddl_GotoPage':1
	}
	postdata=urllib.parse.urlencode(searchData).encode('utf8') #进行编码
	request=Request(url)
	reponse=urlopen(request).read()
	handleData(pageIndex,reponse);

#处理数据
def handleData(pageIndex,pageData):
	bsObj = BeautifulSoup(pageData,"html.parser")
	listObj = bsObj.find(id="ctl00_ctl20_g_010c6b5b_8f5c_4c45_b548_1a5f8e6e8b34_GridViewWebPart").findAll('tr');
	if(len(listObj) > 0):
		insertList = [];
		for item in listObj:
			itemText = item.findAll('td');
			#判断
			if(len(itemText) == 2):
				insertList.append({
					'name' : itemText[0].find('a').get_text(),
					'license' : itemText[1].get_text()
				})
		print(insertList);
		# insertMongo(pageIndex,insertList);

#数据入库
def insertMongo(pageIndex,insertList):
	client = MongoClient("mongodb://localhost:27017/")
	db = client.TjHlicense
	db.posts.insert(insertList)
	client.close();
	#一轮完成并给予提示
	print(pageIndex,':end');
	#沉睡后再跑一波
	delayTimer = random.randint(sleepTimerMin,sleepTimerMax)
	time.sleep(delayTimer)
	pageIndex = pageIndex + 20;
	getData(pageIndex);

#原始数据
pageIndex = 1;
getData(pageIndex);

