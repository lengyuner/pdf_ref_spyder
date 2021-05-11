'''utf-8
    ref：
    [python实战|获取英文文献pdf中参考文献信息](https://www.jianshu.com/p/740ff2f037ee)
'''

import re
# import PyMuPDF
import fitz
import pandas as pd
import numpy as np


# 获取从references开始及之后的页面内容
def GetRefPages(pdfname):
    pdf = fitz.open(pdfname)
    pagenum = len(pdf)
    ref_list = []
    for num, p in enumerate(pdf):
        content = p.getText('blocks')
        # print(num)
        for pc in content:
            # print(pc)
            txtblocks = list(pc[4:-2])
            txt = ''.join(txtblocks)
            if 'References' in txt or 'REFERENCES' in txt or 'referenCes' in txt:
                refpagenum = [i for i in range(num, pagenum)]
                for rpn in refpagenum:
                    refpage = pdf[rpn]
                    refcontent = refpage.getText('blocks')
                    for n, refc in enumerate(refcontent):
                        txtblocks = list(refc[4:-2])
                        ref_list.extend(txtblocks)
    # print(''.join(ref_list))
    return ref_list


# 获取从references之后的文本内容
def GetRefTxt(ref_list):
    refnum = 0
    for nref, ref in enumerate(ref_list):
        if 'References' in ref or 'REFERENCES' in ref or 'referenCes' in ref:
            refnum = nref
    references_list = ref_list[refnum + 1:]
    # print(''.join(references_list))
    return references_list


def process_ref_list(references_list):
    final_list = []
    len_ref = 0
    for K_1 in range(len(references_list)):
        for K_2 in range(len(references_list)):
            if re.match('\[%d\]' % (K_1 + 1), references_list[K_2]):
                # print(K_2)
                len_ref += 1

    for K in range(len_ref):
        if references_list[K][0] == '[':
            final_list.append(references_list[K])
        else:
            final_list[-1] = final_list[-1] + references_list[K]


    # final_list[-1].split('\n')[0]
    for K in range(len(final_list)):
        final_list[K] = final_list[K].replace('-\n', '')
        final_list[K] = final_list[K].replace('\n', ' ')

    # author_list = []
    # title_list = []
    # year_list = []
    ref_data = []
    for reference in final_list:
        try:
            author_end = re.search('[a-z]\.|\?|\! ', reference).span()[1]
            author = reference[0:author_end]
            title_end = re.search('[a-z]\.|\?|\! ', reference[author_end:]).span()[1]
            title = reference[author_end + 1:title_end + author_end]
        except:
            author = 'None'
            title = 'None'
        year = re.findall('19[0-9]{2}|20[0-9]{2}', reference)[0]
        # print(year)

        # author_list.append(re.split('[a-z]\.|\?|\! ', reference)[0])
        # title_list.append(re.split('[a-z]\.|\?|\! ', reference)[1])
        # year_list.append(re.findall('19[0-9]{2}|20[0-9]{2}', reference)[0])
        ref_data.append([author, title, year])
    # ref_data = [author_list, title_list, year_list]
    # return np.asarray(ref_data)
    return ref_data


# re.search('[a-z]\.|\?|\! ', reference)
# re.match('[a-z]\.|\?|\! ', reference)
# re.match('[a-z]\.|\?|\! ', reference)
# def GetUnitRef(references_list):
#     # 去除一些不必要的字符
#     references_list = [i.replace('\n', ' ') for i in references_list]
#     references_list = [re.sub(r'<.*>', '', i) for i in references_list]
#
#     # 将所有文本变成一个字符串
#     references = ' '.join(references_list).replace('- ', '')
#     references = re.sub(r'\([0-9]{1,3}\)', '', references).replace('   ', '')
#     # print(references)
#
#     # 根据 作者（ 通过正则表达式进行拆分
#     # 特殊：Taubman Ben-Ari, O.
#     # 特殊：(in press)
#     authorspattern = re.compile(r'([A-Za-z]+ ?[A-Za-z]* ?[A-Za-z]*-?[A-Za-z]*, [A-Z]\..*?\([0-9|a-zA-Z])')
#     reflist = re.split(authorspattern, references)
#     reflist = list(filter(None, reflist))
#     # print(reflist)
#
#     # 将参考文献导出(略有瑕疵)
#     allref_list = []
#     # 拆分后每2个拼成1条文献，若遇到页眉，则跳过
#     reflength = len(reflist)
#     step = 2
#     for i in range(0, reflength, step):
#         # 若遇到页眉则跳过（页眉的第2条没有.,等符号）
#         if '.' in reflist[i + 1] or '). ' in reflist[i + 1]:
#             unitref = reflist[i:i + step]
#             unit = ''.join(unitref)
#             allref_list.append(unit)
#
#     # 处理书籍参考文献（先前半段和后半段合并进入列表，再删除前半段）
#     mid_list = []
#     for n, a in enumerate(allref_list):
#         if 'Ed' in a and re.search(r'\([0-9]+\)', a) == None:
#             mid_list.append(allref_list[n - 1] + allref_list[n])
#         else:
#             mid_list.append(a)
#
#     final_list = []
#     for num, i in enumerate(mid_list[:-1]):
#         if i not in mid_list[num + 1]:
#             final_list.append(i)
#     final_list.append(mid_list[-1])
#
#     return final_list
#
# final_list = GetUnitRef(references_list)


# for ref in final_list:
#     ref = ref.replace('-\n', '')
#     ref = ref.replace('\n', ' ')
#
# for K in range(len(final_list)):
#     final_list[K] = final_list[K].replace('-\n', '')
#     final_list[K] = final_list[K].replace('\n', ' ')
#

#
# author_list = []
# title_list = []
# year_list = []
# for reference in final_list:
#     # f = final_list[K]
#     # author_specile = re.compile('[A-Z]\.')
#     # print(re.findall(author_specile, f))
#     # print(re.split('[a-z]\. ',reference))
#     # referencelist.append
#     # re.split('[a-z]\.|\?|\! ', reference)
#     # print(re.split('[a-z]\.|\?|\! ', reference))
#     # print(len(re.split('[a-z]\.|\?|\! ',reference)))
#     author_list.append(re.split('[a-z]\.|\?|\! ', reference)[0])
#     title_list.append(re.split('[a-z]\.|\?|\! ', reference)[1])
#     year_list.append(re.findall('19[0-9]{2}|20[0-9]{2}', reference)[0])

# refdata = {
#             'Author': author_list,
#             'Year': year_list,
#             'Title': title_list,
#             # 'Journal':journallist,
#             # 'DOI':doilist,
#             # 'Reference':referencelist
#             }
# refdata=pd.DataFrame(refdata)

# 转为数据框
#         refdata={
#         'Author':authorlist,
#         'Year':yearlist,
#         'Title':titlelist,
#         'Journal':journallist,
#         'DOI':doilist,
#         'Reference':referencelist
#         }
#         refdata=pd.DataFrame(refdata)
#     print(refdata)
#     return refdata


# for reference in final_list:
#     author_special = re.compile('[A-Z]\.')
#     # print(re.findall(author_specile, reference))
#     author_special_all = re.findall(author_special, reference)
#     len(author_special_all)


# f = final_list[4]
# # /^[A-Z][a-z]*(\s[A-Z][a-z]*)*$/
#
# re.findall(r'([A-Za-z]+ ?[A-Za-z]* ?[A-Za-z]*-?[A-Za-z]*, [A-Z]\..*?\()',f)
#
# re.findall(r'([A-Za-z]+ ?[A-Za-z]* ?[A-Za-z]*-?[A-Za-z]*, [A-Z]\..*?\()',f)
#
# re.findall('/^[A-Z][a-z]*(\s[A-Z][a-z]*)*$/',f)
#
# re.findall('[A-Z][a-z]*,', f)
#
#
#
#
# re.findall('[0-9]{2}', f)
#
#
# re.findall('(20[0-9]{2},19[0-9]{2})', f)
#
# f='19023'
# re.findall('19[0-9]{2}', f)
# re.findall('20[0-9]{2}', f)
#
# re.findall('19[0-9]{2}|20[0-9]{2}', f)
#
# year = re.compile('19[0-9]{2}|20[0-9]{2}')
# re.split(year, f)
#
#
# author = re.compile('([A-Za-z]+ ?[A-Za-z]* ?[A-Za-z]*-?[A-Za-z]*, [A-Z]\..*?\()')
#
# author = re.compile('[A-Z][.-z]* [A-Z][.-z]*')
# re.findall(author, f)
#
#
# referencelist=[]
# for reference in final_list:
#     # f = final_list[K]
#     # author_specile = re.compile('[A-Z]\.')
#     # print(re.findall(author_specile, f))
#     print(re.split('[a-z]\. ',reference))
#     # referencelist.append(f)
#
#
#
# f = final_list[5]
# re.findall('[A-Z]\. ', f)

# referencelist=[]
# for f in final_list:
#         # 全文
#         # f = final_list[K]
#         referencelist.append(f)
#         # print(f)
#         # 作者
#         try:
#             author=re.findall(r'([A-Za-z]+ ?[A-Za-z]* ?[A-Za-z]*-?[A-Za-z]*, [A-Z]\..*?\()',f)[0].replace('(','')
#         except:
#             author='Null'
#         authorlist.append(author)

# 从每条参考文献中提取信息
# def GetInfo(final_list):
#     referencelist=[]
#     authorlist,yearlist,titlelist,journallist=[],[],[],[]
#     doilist=[]
#     for f in final_list:
#         # 全文
#         referencelist.append(f)
#         # print(f)
#         # 作者
#         try:
#             author=re.findall(r'([A-Za-z]+ ?[A-Za-z]* ?[A-Za-z]*-?[A-Za-z]*, [A-Z]\..*?\()',f)[0].replace('(','')
#         except:
#             author='Null'
#         authorlist.append(author)
#         # print(len(author),author)
#
#         # 年份
#         try:
#             year=re.findall(r'(\([0-9|a-z| ]+\))',f)[0].replace('(','').replace(')','')
#         except:
#             year='Null'
#         yearlist.append(year)
#         # print(len(year),year)
#
#         # 标题
#         try:
#             title=f.split('). ')[1].replace('?','.').split('.')[0]
#         except:
#             title='Null'
#         titlelist.append(title)
#         # print(len(title),title)
#
#         # 期刊
#         try:
#             # journal=f.split('). ')[1].split('.')[1].split(',')[0]
#             journal=''.join(re.findall(r'.*?\)\. .*?[\.|?] (.*[,|.]?)',f)).split(',')[0]
#         except:
#             journal='Null'
#         journallist.append(journal)
#         # print(len(journal),journal)
#
#         # DOI
#         try:
#             if 'doi.org' in f :
#                 DOI=f.split('org/')[1]
#             elif 'doi:' in f:
#                 DOI=f.split('doi:')[1]
#             else:
#                 DOI='Null'
#         except:
#             DOI='Null'
#         doilist.append(DOI)
#         # print('DOI:',DOI)
#
#         # 转为数据框
#         refdata={
#         'Author':authorlist,
#         'Year':yearlist,
#         'Title':titlelist,
#         'Journal':journallist,
#         'DOI':doilist,
#         'Reference':referencelist
#         }
#         refdata=pd.DataFrame(refdata)
#     print(refdata)
#     return refdata
#
#
# refdata = GetInfo(final_list)


def process_ref_list_old(final_list):
    ref = 1

    # for
    paper_info_all = []
    for K in range(4):
        # print(paper_all[K])
        paper_detail = final_list[K]
        all_info = paper_detail.split('. ')
        paper_info_all.append(all_info[-3:])

        print(all_info)


# 将参考文献文本写入txt
def write2txt(path, filename, final_list):
    txtname = path + '\\' + '[Refs of]' + filename + '.txt'
    with open(txtname, "w", encoding='utf-8') as f:
        txtcontent = '\n'.join(final_list)
        f.write('<<' + filename + '>>' + '\n' + txtcontent)


# 将参考文献信息写入excel
def refinfo2excel(path, filename, refdata):
    excelname = path + '\\' + '[Refs of]' + filename + '.xlsx'
    refdata.to_excel(excelname, index=0)

# [4] Dylan Drover, Ching-Hang Chen, Amit Agrawal, Ambrish Tyagi, and Cong Phuoc
# Huynh. Can 3d pose be learned from 2d projections alone? In
# Proceedings of the European Conference on Computer Vision Workshops (ECCV), pages 0–0, 2018. 3 '


# all_info = paper_detail.split('. ')


# list all the name of journal and conference


# import re
#
# # 使用match方法进行匹配操作
# result = re.match("itcast", "itcast.cn")
# print(result)  # 输出的是一个对象
# # 获取匹配结果
# info = result.group()
# print(info)


if __name__ == '__main__':

    pdf_name = 'Wild.pdf'

    ref_list = GetRefPages(pdf_name)

    references_list = GetRefTxt(ref_list)

    final_list = process_ref_list(references_list)

    ref_csv_name = pdf_name.replace('.pdf', '___ref.csv')

    with open(ref_csv_name, 'w', encoding='utf-8') as f:
        for ref in final_list:
            print(ref)
            line = ref[0].replace(', ', '  ') + ',' + ref[1].replace(', ', ' ') + ',' + ref[2] + ',\n'
            f.write(line)




