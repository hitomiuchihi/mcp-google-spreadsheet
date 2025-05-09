# エントリーポイント

# API経由でアクセス可能なGoogleスプレッドシート情報
accessible_spreadsheets = [
	{
		"sheet_name": "受講生選考状況",
		"discription": "自社のプログラミングスクール受講生の転職活動における選考状況を管理するためのスプレッドシート",
		"sheetUrl": "https://docs.google.com/spreadsheets/d/1LB3QS6peeSwadoguqhuFNfE53euEyQt--mHDoO9b8SY/edit?usp=sharing",	
	},
 {
	 "sheet_name": "Team Ms.メンバー",
	 "discription": "自社プログラミングスクールの卒業生でパートナー企業に派遣されている/される可能性のあるTeam Ms.という組織のメンバー情報を管理するためのスプレッドシート",
   "sheetUrl": "https://docs.google.com/spreadsheets/d/1a8mEaBSPvrGq6lZnrreAIgfmWDDhBtZeAvsOFa2Lu1c/edit?usp=sharing",
 },
 {
	 "sheet_name": "パートナー企業",
	 "discription": "Team Ms.のメンバーがインターンや業務委託という形態で派遣される可能性のある企業の情報を管理するためのスプレッドシート",
   "sheetUrl": "https://docs.google.com/spreadsheets/d/1DHXzO8mUFYX6oMlrVzN6UOFEyxtG-qV27wGPd8rFYcA/edit?usp=sharing",
 },
 {
	 "sheet_name": "受講生アンケート",
	 "discription": "自社プログラミングスクールで現在受講中の受講生がm回収提出するアンケート結果を蓄積、管理しているスプレッドシート",
   "sheetUrl": "https://docs.google.com/spreadsheets/d/1KKUJ8xcVGXevSEM9AnRKAifjZ1_xJsVU487fC6BPu-s/edit?usp=sharing",
 }
]

# google_auth.pyの動作確認コード

# from google_auth import get_sheets_service

# if __name__ == '__main__':
#     sheets_service = get_sheets_service()
#     print("✅ Google Sheets API connected successfully!")

# google_sheet.pyの動作確認コード
from google_sheet import get_all_sheets_data, convert_to_dict_records

if __name__ == "__main__":
    all_data = get_all_sheets_data("パートナー企業")  # スプレッドシート名を指定
    records = convert_to_dict_records(all_data)
    print(records)  # 辞書形式で出力