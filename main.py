from models import Author, Quotes
import connect
import redis
from redis_lru import RedisLRU

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)

@cache
def find_by_tag(tag: str) -> set[str | None]:
    find_tag = tag.split(',')
    for ft in find_tag:
        quotes = Quotes.objects(tags__iregex=ft)
        result = [q.quote for q in quotes]
    return result

@cache
def find_by_author(author: str) -> list[str | None]:
    print(f'Find by {author}')
    authors = Author.objects(fullname__iregex=author)
    result = list()
    for a in authors:
        quotes = Quotes.objects(author=a)
        result.append([q.quote for q in quotes])
    return result

def main():
    while True:
        user_input = input('Enter command: ')
        if user_input == 'exit':
            print('Good bye')
            exit()

        try:
            action = user_input.split(':')[0]
            arg = user_input.split(':')[1].strip()

            match action:
                case 'name':
                    r = find_by_author(arg)
                    print(r)
                case 'tag':
                    r = find_by_tag(arg)
                    print(r)
                case 'tags':
                    r = find_by_tag(arg)
                    print(r)
                case _:
                    print('Unknown command')
        except:
            print('Unknown command')

if __name__ == '__main__':
    main()


