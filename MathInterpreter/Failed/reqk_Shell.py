import reqk_math

if __name__ == "__main__":
    running = True

    while running:
        raw = input(">> ")
        if raw == 'q':
            running = False
        else:
            result, error = reqk_math.main('<stdin>', raw)
            if error:
                print(error)
            else:
                print(result)
