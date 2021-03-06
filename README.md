### Backend for simple web-service to write text on image     

---
Frontend for this project is here - https://github.com/samaranin/add-text-on-image-frontend   

_________________________________________________
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
      "text_image": "image_with_text", 
      "label_image": "label_image", 
      "join": "left" or "right"
   }   
   ```
   and returns path to generated image   
   ```
   {"data": "temp/image.name"}
   ```   
__8. /api/write_text/__ - endpoint to write text on images (image must be on server)        
&nbsp;&nbsp;&nbsp;&nbsp;a. __GET__ method - returns JSON-error with text and example JSON-scheme      
&nbsp;&nbsp;&nbsp;&nbsp;b. __POST__ method - gets JSON   
   ```
   {
      "background_image": "image_to_write_text", // <- must be on server in sources/backgrounds   
      "header": "header",    
      "footer": "footer",   
      "width": "width",    
      "height": "height",    
      "header_font_name": "header_font_name",    // <- must be on server in fonts/
      "text_width_header": "text_width_header",  
      "font_size_header": "font_size_header",    
      "footer_font_name": "footer_font_name",   // <- must be on server in fonts/
      "text_width_footer": "text_width_footer",   
      "font_size_footer": "font_size_footer",   
      "top_padding": "top_padding",   
      "bottom_padding": "bottom_padding"   
   }   
   ```
   and returns path to generated image   
   ```
   {"data": "temp/image.name"}
   ```   
__9. /api/get_image_size/__ - endpoint to get image width and height (must be in sources/labels/ or sources/backgrounds/)      
&nbsp;&nbsp;&nbsp;&nbsp;a. __GET__ method - returns JSON-error with text and example JSON-scheme   
&nbsp;&nbsp;&nbsp;&nbsp;b. __POST__ method - gets JSON   
   ```
   {
      "image_type": "background or label", 
      "image_name": "name of image"
   }   
   ```
   and returns path to generated image   
   ```
   {"widht": "image width", "height": "image height"}
   ```   
__10. /api/remove_temp_files/__ - endpoint clear files in temp/ dir   
____________________________________________
#### Run server   

To run the app use command  

```
docker-compose up -d
```

and go to the ``localhost:5000``
