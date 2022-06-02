# module importation
import streamlit as st
from streamlit import cli as stcli
import sys
from PIL import Image
import pandas as pd
import os
import random
import zipfile36 as zipfile
import shutil


# function for cut image
def image_crop(New_image,nbSubdivition : int = 36) -> list:
      img  = New_image 
      sub = []
      for i in range(nbSubdivition):
          sub.append(img.crop((0,(img.size[1]/nbSubdivition)*i,img.size[0],((img.size[1]/nbSubdivition)*(i+1)))))
      return sub


# function for save all images
def saveAllImage(numeroCalque : str,sub : list,resultat : list,imagePart : str) -> None:
        listeNoConfirmed = ['FDC', 'AFD', 'AFJ']
        for element in ['AF', 'AFS', 'AFSC', 'AFC', 'FS', 'FSC', 'NC', 'FC']:
            os.makedirs('./Dataexport/'+element+'/', exist_ok=True)
        for i in range(len(sub)):
            if element in listeNoConfirmed:
                if imagePart == 'left':
                    sub[i].save('./Dataexport/NC/'+numeroCalque+str(i+1)+'l.jpg')
                else:
                    sub[i].transpose(Image.Transpose.FLIP_LEFT_RIGHT).save(
                        './Dataexport/NC/'+numeroCalque+str(i+1)+'r.jpg')
            else:
                if imagePart == 'left':
                    sub[i].save('./Dataexport/'+resultat[i]+'/'+numeroCalque+str(i+1)+'l.jpg')
                else:
                    sub[i].transpose(Image.Transpose.FLIP_LEFT_RIGHT).save(
                        './Dataexport/'+resultat[i]+'/'+numeroCalque+str(i+1)+'r.jpg')

# function get root path and subdirectories
def get_all_file_paths(directory):
  
    # initializing empty file paths list
    file_paths = []
  
    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
  
    # returning all file paths
    return file_paths  



def main():
    st.set_page_config(
            page_title="Cropping",
            page_icon='✂️',
            layout="wide")
    st.title("✂️ APP CUTTING IMAGE")
    colparametre, colimage, colsub = st.columns([2,1,1])

    # section to apply cropping image and save...
    with colparametre:
        with st.expander('Parameters',expanded=True):
            nom_calque = st.text_input('Layer name:',placeholder="date_Gxx")
            file = st.file_uploader("Import image :",type=['png','jpg'])
            subdivised = st.number_input('Subdivision number',step=1,min_value=8,max_value=36,value=36)
            filexlsx = st.file_uploader('Import excel file :',type='xlsx')
        sub=[]
        
        if file != None:
            image = Image.open(file)
            imagepart = st.radio('Right or left image',options=['left','right'])
            if imagepart == 'left':
                w,h= image.size
                crop_left = st.slider('left',min_value=0,max_value=w,value=260)
                crop_top = st.slider('top',min_value=0,max_value=h,value=350)
                crop_right = st.slider('right',min_value=0, max_value=w,value=645)
                crop_bottom = st.slider('bottom',min_value=0,max_value=h,value=1988)
                if (crop_left < crop_right and crop_bottom > crop_top):
                    NewImage = image.crop((crop_left,crop_top,crop_right,crop_bottom))
                    st.write(NewImage.size)

                    if NewImage.size[0] < image.size[0] and NewImage.size[1] < image.size[1]:
                        st.info("Resolution acceptable")
                        sub = image_crop(NewImage,subdivised)
                        if filexlsx != None:
                            df = pd.read_excel(filexlsx)
                            if st.button('Save'):
                                excel_left = df.iloc[:36,:]
                                try:
                                    saveAllImage(nom_calque,sub,excel_left['resultat'].to_list(),imagepart)
                                    st.success("carry out")
                                except:
                                    st.warning('error')


                    else:
                        st.warning("Adjusted the image")
                else:
                    st.warning("Adjusted the image")
            else:
                w,h= image.size
                crop_left = st.slider('left',min_value=0,max_value=w,value=1023)
                crop_top = st.slider('top',min_value=0,max_value=h,value=350)
                crop_right = st.slider('right',min_value=0, max_value=w,value=1410)
                crop_bottom = st.slider('bottom',min_value=0,max_value=h,value=1984)
                if (crop_right > crop_left and crop_bottom > crop_top):
                    NewImage = image.crop((crop_left,crop_top,crop_right,crop_bottom))
                    st.write(NewImage.size)

                    if NewImage.size[0] < image.size[0] and NewImage.size[1] < image.size[1]:
                        st.info("Resolution acceptable")
                        sub = image_crop(NewImage,subdivised)
                        if filexlsx != None:
                            df = pd.read_excel(filexlsx)
                            if st.button('Save'):
                                excel_rigth = df.iloc[36:,:]
                                try:
                                    saveAllImage(nom_calque,sub,excel_rigth['resultat'].to_list(),imagepart)
                                    st.success("carry out")
                                except:
                                    st.warning('error')

                    else:
                        st.warning("Adjusted the image")
                else:
                    st.warning("Adjusted the image")
        else:
            with st.expander('How to use ?'):
                st.markdown("The application is very simple to use enter the name of the layer, load the image as well as the excel file which is associated with it then check that there is no resolution error while this error will appear adjust the image once Once you adjust the image, you can crop it, don't forget to look at the end section which shows the portion of an image to be cropped, if the portion does not suit you adjust the image, then click save to apply the cut. As in general our images are in two parts, you will do the same exercise from left to right. Then at the top left you have a sidebar for exporting all the images.")
    
    # columns for visualized adjusted image
    with colimage:
        if file != None: 
            if crop_left < crop_right and crop_top < crop_bottom :
                st.image(NewImage)


    # columns for visualized one random image crop
    with colsub:
        if file != None and len(sub) != 0:
            st.markdown('### observe the cut :')
            choix = sub[0]
            if st.button('Next'):
                choix = random.choice(sub)
            st.image(choix)
    
    # sidebar for export all images
    with st.sidebar:
        directory = './Dataexport'
        export = os.path.exists(directory)
        if export == True:
            if st.checkbox('Export all image'):
                file_paths = get_all_file_paths(directory)
                with zipfile.ZipFile('ImageExport.zip','w') as zip:
                    for file in file_paths:
                        zip.write(file)
                if os.path.exists('ImageExport.zip') == True:
                    with open('ImageExport.zip', 'rb') as f:
                        st.download_button('Download Zip', f, file_name='ImageExport.zip')
            if st.button('clear file'):
                shutil.rmtree(directory)
                if os.path.exists('ImageExport.zip') == True:
                    os.remove('ImageExport.zip')

        else:
            st.error('you cannot export . file not generated')


# execute app
if __name__ == '__main__':
    if st._is_running_with_streamlit:
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())