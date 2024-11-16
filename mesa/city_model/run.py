from model import CityModel

city_model = CityModel()

city_model.display_combined_grid()
for i in range(20):
    print(f"Paso {i + 1}")
    city_model.step()
    city_model.display_combined_grid()