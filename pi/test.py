from observable import Observable

obs = Observable()

@obs.on("test")
def test_handler(message):
    print("Test: %s" % message)

obs.trigger("test", "It worked!")
