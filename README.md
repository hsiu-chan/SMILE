# SMILE
## How to run

### Python?

運行[/app/main.py](app/main.py)



### Docker
>Docker 製作中

```shell
cd {dir_path}
```

```shell
docker image build -t smile .
```
```shell
docker run -d -p 7777:8888 --name smile smile
```

停止/移除所有 container
```shell
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
```

## 說明
### 標註
1. SMA 自動產生mask
    - 懶得用flask架成網頁了，只能直接運行 app/BuildTraindata.ipynb
    - input png 照片: app/TrainData/data
1. 手動標註
    - 運行[/app/main.py](app/main.py)
    - 標註介面路徑:[/pages/label](/pages/label)
    - check 後會把標註完的資料送到 [app/TrainData/labeled](/app/TrainData/labeled)
1. 轉換成CoCo資料集
    - 見 BuildCoCoDataset.py, Train.ipynb


### DEMO

1. SMA Demo:[/pages/SMAdemo](/pages/SMAdemo)
    - 檢查 /app/app.py的註解



[Vedio](https://user-images.githubusercontent.com/106435999/236290831-b03c69f1-92e4-4398-9301-e7288f5ceb6f.mp4)

## 參考資料

1. [SMA期末讀論文作業](https://github.com/hsiu-chan/SMILE/blob/main/Document/%E8%AE%80SMA.pdf)
