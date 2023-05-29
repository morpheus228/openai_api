from models import ChatModel


def choose_place_by_request(model: ChatModel, places: dict, request: str):
    input_content = f"Выбери из следующих трех мест:\n" \
                    f"1. {places[1]}\n\n" \
                    f"2. {places[2]}\n\n" \
                    f"3. {places[3]}\n\n" \
                    f"более подходящее следующему запросу: {request}\n" \
                    f"Напиши номер этого места."

    return model.make_request(user_content=input_content)
