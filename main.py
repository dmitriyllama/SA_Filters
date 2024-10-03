import cv2
from processing import VideoFileSource, Display, GrayscaleFilter, MirrorFilter, ResizeFilter, ColorFilter

video_file = 'example.mp4'

# Sink
out_display_1 = Display('Output Grayscale', outputs=[])
out_display_2 = Display('Output Recolored', outputs=[])

# Filters
grayscale = GrayscaleFilter(outputs=[out_display_1.show])
recolor = ColorFilter(outputs=[out_display_2.show], code=cv2.COLOR_RGB2BGR)

mirror = MirrorFilter(outputs=[grayscale.input, recolor.input])
resize = ResizeFilter(outputs=[mirror.input], x=512, y=256)

# Source
in_display = Display('Input', outputs=[resize.input])
in_reader = VideoFileSource(video_file, outputs=[in_display.show])


in_reader.start()

cv2.destroyAllWindows()