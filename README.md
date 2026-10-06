# zip-index

自己解析 ZIP 的中央目录，列出条目表。只用 Python 标准库，**不许调用 `zipfile` / `zipimport`**。

```
python3 -m unittest discover -s tests
python3 -m zipindex dump --file a.zip
python3 -m zipindex --sample=prefix|extra|count|work
```

## 口径

- **定位**：从文件末尾找 EOCD 记录（签名 `0x06054b50`），用它的中央目录偏移与条数定位，允许文件前面有自解压前缀。
- **条目**：每条中央目录记录签名 `0x02014b50`，名字长度在记录内第 28 字节起，名字后面还跟着扩展字段与注释。
- **条数**：只读 EOCD 声明的那几条，多出来的记录不算。
- **字段**：每条给出 `name`、`method`、`crc`、`csize`、`usize`。

## 不变量

- 条目数与 EOCD 声明一致，不会越读。
- 名字按 UTF-8 解码。
- `scanned` 不随条目数乘查询次数放大：两千条条目查两千次的 `scanned` 不超过 9000。

## 输出契约

`dump` 打印对齐表格，列顺序为 `name`、`method`、`crc`、`csize`、`usize`，末行是 `{"entries": N}`。
`--sample=work` 只打印 `{"entries": N, "scanned": N}`。
