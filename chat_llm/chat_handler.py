import re
from openai import OpenAI


class ChatHandler:
    def __init__(self, api_key: str, hexcodes: tuple):
        """
        Initializes the ChatHandler with OpenAI API key and facial feature hexcodes.

        Parameters:
            api_key (str): OpenAI API key.
            hexcodes (tuple): A tuple containing hexcodes for facial features in the order:
                (left_eye_colour, right_eye_colour, nose_colour, jaw_colour, lips_colour).
        """
        self.client = OpenAI(api_key=api_key)
        self.left_eye_colour = hexcodes[0]
        self.right_eye_colour = hexcodes[1]
        self.nose_colour = hexcodes[2]
        self.jaw_colour = hexcodes[3]
        self.lips_colour = hexcodes[4]

    def get_good_palette(self):
        """
        Provides a good color palette based on user's facial features.

        Returns:
            dict: A dictionary containing hexcodes and corresponding color names for the palette.
        """
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_format={"type": "text"},
            messages=[
                {
                    "role": "system",
                    "content": "You are a fashion assistant and a cosmetic advisor. Answer the user's questions about fashion and cosmetics . you have to answer in the format of the given example",
                },
                {
                    "role": "user",
                    "content": f"My facial features hexcodes are left eye colour =={self.left_eye_colour}, right eye colour =={self.right_eye_colour}, nose colour =={self.nose_colour}, jaw colour =={self.jaw_colour}, and lips colour =={self.lips_colour}.",
                },
                {
                    "role": "user",
                    "content": """I want to know which 5 colours will look good on me and why? be creative and answer in the given format,  example: 
                    1. #f4e1cb (peach): Peach complements your warm facial features and will give you a fresh and radiant look. It will be perfect for summers with its soft and delicate hue.
                    2. #4b86b4 (steel blue): Steel blue will enhance the cool tones in your eyes and create a striking contrast with your warm facial features. This color is versatile and can be worn in both casual and formal settings.
                    3. #f9c1bb (coral pink): Coral pink will bring out the rosy tones in your lips and cheeks. This vibrant color will add a pop of energy to your look and is ideal for a fun and playful vibe.
                    4. #82647a (mauve): Mauve will complement the subtle tones in your nose and jaw area. This elegant and understated color is perfect for a sophisticated and chic look, ideal for evenings out or special occasions.
                    5. #ffd966 (mustard yellow): Mustard yellow will enhance the warmth in your facial features and add a touch of sunshine to your overall appearance. This bold and unconventional color choice will make you stand out and exude confidence and individuality.
                    """,
                },
            ],
        )
        return response.choices[0].message.content

    def get_bad_palette(self):
        """
        Provides a bad color palette that would not suit the user based on their facial features.

        Returns:
            dict: A dictionary containing hexcodes and corresponding color names for the palette.
        """
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_format={"type": "text"},
            messages=[
                {
                    "role": "system",
                    "content": "You are a fashion assistant and a cosmetic advisor. Answer the user's questions about fashion and cosmetics. you have to answer in the format of the given example",
                },
                {
                    "role": "user",
                    "content": f"My facial features hexcodes are left eye colour =={self.left_eye_colour}, right eye colour =={self.right_eye_colour}, nose colour =={self.nose_colour}, jaw colour =={self.jaw_colour}, and lips colour =={self.lips_colour}.",
                },
                {
                    "role": "user",
                    "content": """I want to know which 5 colours will NOT complement me and why? be creative but never be rude and answer in the given format,  example:
                    1. #687864 (Sage Green) - This cool-toned green might clash with the warm tones of your eye, nose, and lip colors, creating a dissonance in your overall look.
                    2. #874c62 (Mauve) - The muted pink undertones of mauve might make your lip color appear dull in comparison, not accentuating your natural features.
                    3. #433d4f (Charcoal Gray) - The deep gray might overpower the softness of your jaw and nose colors, creating a mismatched look that doesn't enhance your natural beauty.
                    4. #b28975 (Mocha) - The brown undertones of mocha might blend in too much with your jaw color, making your features appear flat and lacking dimension.
                    5. #91a8d0 (Periwinkle Blue) - The cool-toned blue might not harmonize well with the warm hues of your eyes and lips, potentially washing out your complexion and not bringing out your best features. 
                    """,
                },
            ],
        )
        return response.choices[0].message.content

    def get_blush(self):
        """
        Provides detailed information about the suitable blush colors based on the color of user's lips.

        Returns:
            str: A string containing detailed information about the suitable blush colors.
        """
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_format={"type": "text"},
            messages=[
                {
                    "role": "system",
                    "content": "You are a fashion assistant and a cosmetic advisor. Answer the user's questions about fashion and cosmetics. you have to answer in the format of the given example",
                },
                {
                    "role": "user",
                    "content": f"My facial features hexcodes of lips is {self.lips_colour}.",
                },
                {
                    "role": "user",
                    "content": """I want to know which 5 colours will look good on me and why be creative and answer in the given format,  example:
                    1. #FFFFFF (White): White will provide a striking contrast to your lip color, making it pop even more. It represents purity and simplicity and will give you a fresh and clean look.
                    2. #2a9d8f (Teal): Teal is a cool and calming color that will complement the warmth of your lip color. It represents tranquility and balance and will give your overall look a modern and sophisticated edge.
                    3. #f9c22e (Mustard Yellow): Mustard yellow will add a vibrant touch to your look. It represents energy and positivity and will bring a fun and playful element to your outfit.
                    4. #6b5b95 (Lavender): Lavender is a soft and romantic color that will enhance the femininity of your lip color. It represents grace and elegance and will give your look a dreamy and whimsical vibe.
                    5. #e07a5f (Terracotta): Terracotta is an earthy and warm color that will harmonize beautifully with your lip color. It represents strength and stability and will give your outfit a grounded and natural feel.
                    """,
                },
            ],
        )
        return response.choices[0].message.content


if __name__ == "__main__":
    # Example usage
    chat_handler = ChatHandler(
        api_key="####",
        hexcodes=("#dfb8aa", "#c39e8e", "#d09d82", "#e4c1ad", "#c34a5b"),
    )
    print(chat_handler.get_good_palette())
    print(chat_handler.get_bad_palette())
    print(chat_handler.get_blush())
