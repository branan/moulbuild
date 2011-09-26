import targets
import dispatcher

def build():
    for t in targets.targets:
        dispatcher.dispatch(t)

if __name__ == "__main__":
    build()