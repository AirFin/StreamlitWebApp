# import packages
# data preprocessing
import pandas as pd
import numpy as np

# plotting
import plotly.express as px

# extra libraries
import translators as ts
import textdistance
import streamlit as st

tab1, tab2 = st.tabs(["主页面", "算法选择说明"])
with tab1:
    
    # APP标题
    st.title("各翻译软件文本相似度比较")

    # 要翻译的文本
    text = st.text_input("请输入中文文本", "今天万里无云，风和日丽。")
    # 选择文本相似度计算方法
    algorithm = st.text_input("请输入文本相似度计算方法", "hamming")
    st.warning("更多算法请复制**算法选择说明**页面**Functions**列中的内容到此处")
    st.markdown("---")

    # 翻译软件列表
    list_transitions = ["baidu", "youdao", "bing", "caiyun", "alibaba"]

    # 一个开始运行的按钮
    button_start = st.button("开始")
    if button_start==True:
        # 此处代码的结果会生成各翻译软件的翻译结果，如：result_baidu、result_youdao
        for transition in list_transitions:
            exec(f'result_{transition} = ts.{transition}(text, from_language="auto", to_language="en")')

        # 展示各翻译软件的翻译结果
        st.markdown("## 翻译结果")
        st.write(f"百度翻译结果：{result_baidu}")
        st.write(f"有道翻译结果：{result_youdao}")
        st.write(f"必应翻译结果：{result_bing}")
        st.write(f"彩云翻译结果：{result_caiyun}")
        st.write(f"阿里翻译结果：{result_alibaba}")
        st.markdown("---")
        
        # 计算文本相似度
        list_text = [result_baidu, result_youdao, result_bing, result_caiyun, result_alibaba]


        # calculate the similarity between each pair of texts
        # 注意这里的写法，注意缩进！不然会报错
        exec(
f'''
similarity_matrix = np.zeros((len(list_text), len(list_text)))
for i in range(len(list_text)):
    for j in range(len(list_text)):
        similarity_matrix[i, j] = textdistance.{algorithm}.normalized_similarity(list_text[i], list_text[j])
'''
        )

        # 热力图可视化展示
        st.markdown("## 翻译结果文本相似度热力图")
        heatmap = px.imshow(similarity_matrix,
                        x=list_transitions,
                        y=list_transitions,
                        text_auto='.2f',
                        color_continuous_scale=px.colors.sequential.Blues)

        heatmap

    else:
        st.write("请点击开始按钮")

with tab2:
    st.title("算法选择说明")
    st.markdown('''本页内容来自https://github.com/life4/textdistance 
    
点击Algorithm列的超链接可查看各算法详细说明
    
### Edit based

| Algorithm                                                    | Class                | Functions              |
| ------------------------------------------------------------ | -------------------- | ---------------------- |
| [Hamming](https://en.wikipedia.org/wiki/Hamming_distance)    | `Hamming`            | `hamming`              |
| [MLIPNS](http://www.sial.iias.spb.su/files/386-386-1-PB.pdf) | `Mlipns`             | `mlipns`               |
| [Levenshtein](https://en.wikipedia.org/wiki/Levenshtein_distance) | `Levenshtein`        | `levenshtein`          |
| [Damerau-Levenshtein](https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance) | `DamerauLevenshtein` | `damerau_levenshtein`  |
| [Jaro-Winkler](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance) | `JaroWinkler`        | `jaro_winkler`, `jaro` |
| [Strcmp95](http://cpansearch.perl.org/src/SCW/Text-JaroWinkler-0.1/strcmp95.c) | `StrCmp95`           | `strcmp95`             |
| [Needleman-Wunsch](https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm) | `NeedlemanWunsch`    | `needleman_wunsch`     |
| [Gotoh](http://bioinfo.ict.ac.cn/~dbu/AlgorithmCourses/Lectures/LOA/Lec6-Sequence-Alignment-Affine-Gaps-Gotoh1982.pdf) | `Gotoh`              | `gotoh`                |
| [Smith-Waterman](https://en.wikipedia.org/wiki/Smith%E2%80%93Waterman_algorithm) | `SmithWaterman`      | `smith_waterman`       |

### Token based

| Algorithm                                                    | Class        | Functions                           |
| ------------------------------------------------------------ | ------------ | ----------------------------------- |
| [Jaccard index](https://en.wikipedia.org/wiki/Jaccard_index) | `Jaccard`    | `jaccard`                           |
| [Sørensen–Dice coefficient](https://en.wikipedia.org/wiki/S%C3%B8rensen%E2%80%93Dice_coefficient) | `Sorensen`   | `sorensen`, `sorensen_dice`, `dice` |
| [Tversky index](https://en.wikipedia.org/wiki/Tversky_index) | `Tversky`    | `tversky`                           |
| [Overlap coefficient](https://en.wikipedia.org/wiki/Overlap_coefficient) | `Overlap`    | `overlap`                           |
| [Tanimoto distance](https://en.wikipedia.org/wiki/Jaccard_index#Tanimoto_similarity_and_distance) | `Tanimoto`   | `tanimoto`                          |
| [Cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity) | `Cosine`     | `cosine`                            |
| [Monge-Elkan](https://www.academia.edu/200314/Generalized_Monge-Elkan_Method_for_Approximate_Text_String_Comparison) | `MongeElkan` | `monge_elkan`                       |
| [Bag distance](https://github.com/Yomguithereal/talisman/blob/master/src/metrics/bag.js) | `Bag`        | `bag`                               |

### Sequence based

| Algorithm                                                    | Class               | Functions            |
| ------------------------------------------------------------ | ------------------- | -------------------- |
| [longest common subsequence similarity](https://en.wikipedia.org/wiki/Longest_common_subsequence_problem) | `LCSSeq`            | `lcsseq`             |
| [longest common substring similarity](https://docs.python.org/2/library/difflib.html#difflib.SequenceMatcher) | `LCSStr`            | `lcsstr`             |
| [Ratcliff-Obershelp similarity](https://en.wikipedia.org/wiki/Gestalt_Pattern_Matching) | `RatcliffObershelp` | `ratcliff_obershelp` |

### Compression based

[Normalized compression distance](https://en.wikipedia.org/wiki/Normalized_compression_distance#Normalized_compression_distance) with different compression algorithms.

Classic compression algorithms:

| Algorithm                                                    | Class       | Function     |
| ------------------------------------------------------------ | ----------- | ------------ |
| [Arithmetic coding](https://en.wikipedia.org/wiki/Arithmetic_coding) | `ArithNCD`  | `arith_ncd`  |
| [RLE](https://en.wikipedia.org/wiki/Run-length_encoding)     | `RLENCD`    | `rle_ncd`    |
| [BWT RLE](https://en.wikipedia.org/wiki/Burrows%E2%80%93Wheeler_transform) | `BWTRLENCD` | `bwtrle_ncd` |

Normal compression algorithms:

| Algorithm                                                    | Class        | Function      |
| ------------------------------------------------------------ | ------------ | ------------- |
| Square Root                                                  | `SqrtNCD`    | `sqrt_ncd`    |
| [Entropy](https://en.wikipedia.org/wiki/Entropy_(information_theory)) | `EntropyNCD` | `entropy_ncd` |

Work in progress algorithms that compare two strings as array of bits:

| Algorithm                                  | Class     | Function   |
| ------------------------------------------ | --------- | ---------- |
| [BZ2](https://en.wikipedia.org/wiki/Bzip2) | `BZ2NCD`  | `bz2_ncd`  |
| [LZMA](https://en.wikipedia.org/wiki/LZMA) | `LZMANCD` | `lzma_ncd` |
| [ZLib](https://en.wikipedia.org/wiki/Zlib) | `ZLIBNCD` | `zlib_ncd` |

See [blog post](https://articles.life4web.ru/other/ncd/) for more details about NCD.

### Phonetic

| Algorithm                                                    | Class    | Functions |
| ------------------------------------------------------------ | -------- | --------- |
| [MRA](https://en.wikipedia.org/wiki/Match_rating_approach)   | `MRA`    | `mra`     |
| [Editex](https://anhaidgroup.github.io/py_stringmatching/v0.3.x/Editex.html) | `Editex` | `editex`  |

### Simple

| Algorithm           | Class      | Functions  |
| ------------------- | ---------- | ---------- |
| Prefix similarity   | `Prefix`   | `prefix`   |
| Postfix similarity  | `Postfix`  | `postfix`  |
| Length distance     | `Length`   | `length`   |
| Identity similarity | `Identity` | `identity` |
| Matrix similarity   | `Matrix`   | `matrix`   |

''')



