# Discord-Inactive-Check-Bot
檢測伺服器是否有不活躍的使用者，並把他們列出來 。  

# 安裝

## 使用docker
  1. 複製存儲庫
  ```
  git clone https://github.com/bobo4545/Discord-Inactive-Check-Bot.git
  cd Discord-Inactive-Check-Bot
  ```
  2. 編輯好.env後輸入以下命令，進行容器的構建和啟動
  ```
  docker-compose up --build -d
  ```
  3. 已經構建了容器不需要重新構建，執行以下命令啟動機器人
  ```
  docker-compose up -d
  ```

## 本地安裝
  1. 複製存儲庫
  ```
  git clone https://github.com/bobo4545/Discord-Inactive-Check-Bot.git```
  cd Discord-Inactive-Check-Bot
  ```
  2. (可選) 創建一個虛擬環境並啟動它
  ```
  python -m venv dicb
  source dicb/bin/activate  # 在Unix或Mac OS上
  dicb\Scripts\activate  # 在Windows上
  ```
  3. 安裝依賴項
  ```
  pip install -r requirements.txt
  ```
  4. 啟動機器人
  ```
  python main.py
  ```
# 指令

## !update_db

將伺服器的使用者都列在Activity.json裡，並記錄當下的時間為最後活躍時間

## !check

確認有哪些使用者是不活躍的

# .env設定

TOKEN=輸入你的token
GUILD_ID=輸入你的伺服器ID
INACTIVE_DAYS=輸入不活躍的天數
