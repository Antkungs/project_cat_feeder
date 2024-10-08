def convert_value_to_cm(value):
    try:
        max_cm = 29
        min_cm = 19
        if value >= max_cm:
            value = 29
        elif value <= min_cm:
            value = 19
        return ((value-max_cm)/(min_cm-max_cm))*100

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# ทดสอบการแปลงค่า
print(convert_value_to_cm(29))   # 29
