# Word Cloud MVC


## Uso
1. Instala las dependencias: ```pip install -r requirements.txt```
2. Inicia la aplicación: ```python3 src/mvc_app.py``` o ```py src/mvc_app.py```

## Desarrollo

### Requerimientos de desarrollo

- Instala `QT-Designer`
  1. Descarga el instalador de [QT-Designer](https://build-system.fman.io/qt-designer-download).

### Estructura del proyecto

``` 
project/
    mvc_app.py                     # punto de inicio de la aplicación
    controllers/
        main_controller.py         # controlador principal
        other_controller.py        # otro controlador (en caso de agregar más)    
    model/
        list_model.py              # clase modelo
        word_cloud.py              # clase para generar la nube de palabras
    resources/
        main_view.ui               # archivos generados por qt designer
        other_view.ui              # otro archivo generado (en caso de agregar más)
        img/                       # en caso de agregar imágenes o íconos
    views/
        main_view.py               # vista principal
        main_view_generated_ui.py  # archivo ui autogenerado (usando pyuci5)
        other_view.py              # otra ventana (en caso de agregar más)
        other_view_ui.py           # otro arhivo generado (en caso de agregar más)
```
### Agregar vistas

Para seguir modificando las vistas desde Qt Designer, hay que ubicar el directorio ```.\resources```, aquí se encuentran los arhivos que reconoce Qt Desginer, note la extensión ```.ui```, una vez efectuado algún cambio en Qt Designer, hay que ejecutar el comando ```pyuci5``` para convertir el archivo con extensión ```.ui``` a código ```python```, el archivo generado de python se colocará en la carpeta ```.\view```. Esto se hace usando el párametro ```-x``` seguido del archivo a convertir, es decir, ```.\resources\main_view.ui``` y ```-o``` seguido del archivo a generar, es decir, ```.\view\main_view_generated_ui.py```. Tal como se muestra en el siguiente ejemplo.
```sh
pyuic5 -x .\resources\main_view.ui -o .\view\main_view_generated_ui.py
```
> Nota: Ten cuidado al poner el nombre del archivo a generar de python, ya que puedes sobreescribir algún archivo existente.


