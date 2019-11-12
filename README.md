### Backend for simple web-service to write text on image   


#### Requirements:   

```
flask   
uwsgi   
nider   
flask-cors   
``` 
_________________________________________________
Clone the repository and create next folders   

```
/repository   
--/fonts   
--/temp   
--/sources   
----/backgrounds   
----/labels   
...   
all other code here   
```

_________________________________________
#### Resources description:   
__/fonts__ - folder for fonts   
__/temp__ - folder for processed images   
__/sources__ - folder for source images   
__--/backgrounds__ - images to place text on   
__--/labels__ - images to be attached to backgrounds (to left or right side)   

_________________________________________
#### API Endpoints:   
__1. /api/fonts/__ - list of font files   
__2. /api/backgrounds/__ - list of images to place text on   
__3. /api/labels/__ - list of images to be attached to background   
__4. /sources/backgrounds/image.name__ - endpoint to show background image   
__5. /sources/labels/image.name__ - endpoint to show label image   
__6. /temp/image.name__ - endpoint to show ready image   
__7. /api/join_images/__ - endpoint to join two images (both must be on server, label must be in sources/labels/)      
&nbsp;&nbsp;&nbsp;&nbsp;a. __GET__ method - returns JSON-error with text and example JSON-scheme   
&nbsp;&nbsp;&nbsp;&nbsp;b. __POST__ method - gets JSON   
   ```
   {
      "image1": "image_with_text", 
      "image2": "label_image", 
      "join": "left" or "right"
   }   
   ```
   and returns path to generated image   
   ```
   {"data": "temp/image.name"}
   ```   
__7. /api/write_text/__ - endpoint to write text on images (image must be on server)        
&nbsp;&nbsp;&nbsp;&nbsp;a. __GET__ method - returns JSON-error with text and example JSON-scheme      
&nbsp;&nbsp;&nbsp;&nbsp;b. __POST__ method - gets JSON   
   ```
   {
      "image": "image_to_write_text", // <- must be on server in sources/backgrounds   
      "header": "header",    
      "paragraph": "paragraph",    
      "footer": "footer",   
      "font_name": "font_name",     // <- must be on server in fonts/
      "width": "width",    
      "height": "height",    
      "text_width_header": "text_width_header",  
      "font_size_header": "font_size_header",    
      "text_width_paragraph": "text_width_paragraph",    
      "font_size_paragraph": "font_size_paragraph",    
      "font_size_footer": "font_size_footer"   
   }   
   ```
   and returns path to generated image   
   ```
   {"data": "temp/image.name"}
   ```
   
____________________________________________
#### Run server   

To run the app use command  

```
docker-copmose up -d
```

and go to the ``localhost:5000``