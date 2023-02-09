# Run application

## Creating Virtual Enviroment (VENV)
```
python3 -m venv venv
```

## Activating VENV
```
source venv/bin/activate
```

## Installing libraries
```
pip install -r requirements.in
```

## Running API
```
python3 main.py
```


## Montando imagem
```
docker build -t waiwaitapota-api . 
```

## [Criando network](https://docs.docker.com/engine/reference/commandline/network_create/)
```
docker network create -d bridge waiwainetwork
```

## Executando imagem
```
docker run --network=waiwainetwork 
```