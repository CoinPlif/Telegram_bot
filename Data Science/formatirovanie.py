def your_favorite_color(my_color,**kwargs):
    if "color" in kwargs:
        print("My favorite color is {}, but {} is also pretty good!".format(my_color, kwargs["color"]))
    else:
        print("My favorite color is {}, what is your favorite color?".format(my_color))
your_favorite_color("green", color="yellow", age="18", favourite_film="Star Wars")