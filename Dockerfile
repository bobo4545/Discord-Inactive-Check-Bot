# 使用官方 Python 運行時作為父圖像
FROM python:3.8

# 設置工作目錄
WORKDIR /usr/src/app

# 將當前目錄內容複製到容器中的工作目錄
COPY . .

# 安裝 requirements.txt 中的所有依賴
RUN pip install --no-cache-dir -r requirements.txt

# 定義環境變數
ENV TOKEN your_token_here
ENV GUILD_ID your_guild_id_here

# 運行 bot.py 當容器啟動
CMD [ "python", "./main.py" ]
