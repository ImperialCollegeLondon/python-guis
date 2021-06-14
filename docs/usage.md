# Running the examples

The GUI examples live in different subfolder of `python_guis`, one for each GUI framework. There are three examples in each case:

- A minimum working example - equivalent to a "Hello World" for GUIs.
- An example about plotting data, embedding a matplotlib plot within the GUI.
- A full featured application, requiring the user to provide some inputs, performing some calculation and plotting the results. 

In the case of `kivy` there are two extra examples about doing the same thing but using the `kv` declarative language for designing the GUI. 

For `tkinter` and `kivy`, you can run the examples directly in the terminal (assuming your virtual environment is activated), eg.:

```bash
python python_guis/tkinter/plot_tkinter.py
```

For `jupyter widgets` you need to open the notebook with `jupyter`, eg.:

```bash
jupyter notebook  python_guis/jupyter_widgets/plot_jupyter_widgets.ipynb  
```

As the repository has been installed in edit mode, you can modify any of the examples and run them again in the same way to try new features.