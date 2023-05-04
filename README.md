# SMILE
## How to run
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
