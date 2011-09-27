import targets
import dispatcher

def build():
    for t in targets.targets:
        dispatcher.dispatch(t)

if __name__ == "__main__":
    try:
        build()
    except OSError as e:
        print e.strerror
