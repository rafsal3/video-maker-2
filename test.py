# from textvideo import create_video_for_single_keyword
# from searchandsave import search_and_save_image_google,search_and_save_image_unsplash,search_and_save_GIF
from searchbytype import search_and_save_by_type




if __name__ == "__main__":
    # output_path = "output/image3.mp4"
    # create_video_for_single_keyword("Hello world",output_path ,font_color=(0,0,0),bg_color=(255, 255, 255))
    # search_and_save_image_google("elon musk",output_path)
    # search_and_save_image_unsplash("elon musk",output_path)
    # search_and_save_GIF("elon musk smile",output_path)
    search_and_save_by_type("keyword.json")