
import os
from util import GetRefPages, GetRefTxt, process_ref_list

# ref_data = [author_list, title_list, year_list]

# final_list_1= {}
# final_list_1['author']= author_list
# final_list_1['title'] = title_list
# final_list_1['year'] = year_list

# import numpy as np
# a= np.asarray(final_list)


if __name__ == '__main__':

    single_paper = 0
    if single_paper:
        pdf_name = r'C:\Users\Admin\Desktop\CVPR2021\CanonPose：Self-supervised Monocular 3D Human Pose Estimation in the Wild.pdf'

        ref_list = GetRefPages(pdf_name)
        references_list = GetRefTxt(ref_list)
        final_list = process_ref_list(references_list)

        ref_csv_name = pdf_name.replace('.pdf', '___ref.csv')
        with open(ref_csv_name, 'w', encoding='utf-8') as f:
            for ref in final_list:
                print(ref)
                line = ref[0].replace(', ', '  ') + ',' + ref[1].replace(', ', ' ') + ',' + ref[2] + ',\n'
                f.write(line)
    else:
        fold_name = 'C:/Users/Admin/Desktop/CVPR2021'
        ref_csv_name = os.path.join(fold_name, 'reference_list.csv')
        index = 0
        with open(ref_csv_name, 'w', encoding='utf-8') as f:
            for pdf_name in os.listdir(fold_name):
                if pdf_name[-4:] == '.pdf':
                    print(pdf_name)
                    # pdf_name = 'Cross-domain adapta tion for animal pose estimation.pdf'
                    pdf_name_new = os.path.join(fold_name, pdf_name)
                    ref_list = GetRefPages(pdf_name_new)
                    references_list = GetRefTxt(ref_list)
                    final_list = process_ref_list(references_list)

                    for ref in final_list:
                        print(ref)
                        index += 1
                        line = str(index) + ',' + ref[0].replace(', ', '  ') + ',' + ref[1].replace(', ', ' ') + ',' + \
                               ref[2]+', '+ pdf_name + ',\n'
                        f.write(line)










