# i18n-offline

Run:

```
docker build -t i18n .
docker run -d --rm -p 8181:8181 --name i18n i18n
```

Use:

```
curl -s localhost:8181/en-zh -d '{"Content":"The quick brown fox jumps over the lazy dog"}' | jq .
{
  "Result": "快速棕色狐狸跳过懒懒狗"
}

curl -s localhost:8181/zh-en -d '{"Content":"维基百科是一个多语言、内容自由、任何人都能参与的协作计划，其目标是建立一个完整、准确且中立的百科全书。 "}' | jq .
{
  "Result": "Wikipedia is a multilingual, content-free and collaborative programme in which anyone can participate, with the goal of creating a complete, accurate and neutral encyclopedia."
}
```

For more models, see <https://huggingface.co/Helsinki-NLP>.
