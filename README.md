# SMILE
## How to run
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

## DEMO


https://user-images.githubusercontent.com/106435999/236290831-b03c69f1-92e4-4398-9301-e7288f5ceb6f.mp4

