# i18n-offline

Run:

```
docker build -t i18n .
docker run -d --rm -p 8765:8765 --name i18n i18n
```

Use:

```
echo 'The quick brown fox jumps over the lazy dog' | websocat --no-line -n ws://127.0.0.1:8765/en-zh
快速棕色狐狸跳过懒懒狗

echo '维基百科是一个多语言、内容自由、任何人都能参与的协作计划，其目标是建立一个完整、准确且中立的百科全书。' | websocat --no-line -n ws://127.0.0.1:8765/zh-en
Wikipedia is a multilingual, content-free and collaborative programme in which anyone can participate, with the goal of creating a complete, accurate and neutral encyclopedia.
```

Use as a command in terminal:

![i18n-offline](https://github.com/user-attachments/assets/3e535b60-33e3-47b2-ad0d-a26e6a64a0db)

Use in a web page:

![i18n-web](https://github.com/user-attachments/assets/934acc54-9d9d-42ff-89a2-287a74ec006a)

For more models, see <https://huggingface.co/Helsinki-NLP>.

Server requirement: at least 2GB memory and 10GB free space.
