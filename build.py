import targets
import dispatcher

verbose_except = True

def build():
    try:
        for t in targets.targets:
            dispatcher.dispatch(t)
    except OSError as e:
        if (verbose_except):
            raise
        else:
            print e.strerror
    except Exception as e:
        if (verbose_except):
            raise
        else:
            print e

if __name__ == "__main__":
    verbose_except = False
    build()
    
