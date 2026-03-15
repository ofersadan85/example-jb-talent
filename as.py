import asyncio


async def count():
    for i in range(100):
        await asyncio.sleep(0.01)
        print(i)


async def main():
    print("HELLO FROM MAIN")
    await count()
    print("COUNT IS DONE")


def run_main_twice():
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.create_task(main())
    loop.run_forever()


run_main_twice()
