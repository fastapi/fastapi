# Authorization on FastAPI with Casbin

## Overview

[Casbin](https://casbin.org/) is an open source authorization library with support for many models (like Access Control Lists or ACLs, Role Based Access Control or RBAC, Restful, etc) and with implementations on several programming languages (ie: Python, Go, Java, Rust, Ruby, etc).
It consists of two configuration files:

- A model file: a CONF file (with .conf extension) which specifies the authorization model to be applied (in this case we will use Restful one)
- A policy file: a CSV file that list API methods permissions for each user.

## Steps
1. Install casbin python package with pip

    `pip install casbin`

2. Define Conf policy

    Create new file called **model.conf** with the following content:
    ```
        [request_definition]
        r = sub, obj, act

        [policy_definition]
        p = sub, obj, act

        [policy_effect]
        e = some(where (p.eft == allow))

        [matchers]
        m = r.sub == p.sub && keyMatch(r.obj, p.obj) && regexMatch(r.act, p.act)
    ```
    You can find more details about the syntax of Casbin from [casbin doc](https://casbin.org/docs/overview)
3. Define Policy file
    Create a new CSV file called policy.csv and paste the following:
    ```
        p, alice, /items/*, (GET)|(DELETE)|(POST)
        p, alice, /items, (GET)
        p, johndoe, /items/*, (GET)|(POST)
        p, johndoe, /items, (GET)
    ```
    Each row is an allowed permissions with the following values: the second column is the user, the third is the API resource or url, and the last one is a set of allowed methods. In this case, alice will have access to list create and delete items, while johndoe may list and create items but not delete them.

4. Update Python API code to enforce authorization.
    In the main.py file, with following lines:
    ```
    import casbin
    ...
    async def get_current_user_authorization(req: Request, curr_user: User = Depends(get_current_active_user)):
        e = casbin.Enforcer("model.conf", "policy.csv")
        sub = curr_user.username
        obj = req.url.path
        act = req.method
        if not(e.enforce(sub, obj, act)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Method not authorized for this user")
        return curr_user
    ```
    It imports the casbin module and create a new authorization function that read the configuration files with `casbin.Enforcer` and enforce the user has the required permission.

    Then, on the defined API methods, change the old method `get_current_active_user` with the new `get_current_user_authorization`
    ```
    @app.get("/items/{item_id}")
    async def read_item(item_id: int, req: Request, curr_user: User = Depends(get_current_user_authorization)):
        return items_dao.get_item(item_id)

    @app.post("/items/")
    async def create_item(item: Item, req: Request, curr_user: User = Depends(get_current_user_authorization)):
        answer = items_dao.create_item(item)
        if not(answer):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item with given id already exists")
        else:
            return answer

    @app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_item(item_id: int, req: Request, curr_user: User = Depends(get_current_user_authorization)):
        items_dao.delete_item(item_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    ```

## Test
1. Start the updated API
2. Open http://127.0.0.0:8000/docs url in browser.
3. Click on "Authorize" and login with "johndoe".
4. Try to delete item with id=1. It will be rejected with a 401 Unauthorized error.
5. Logout from that user. Then login with "alice".
6. Try to delete item with id=1. The request works fine, returns 204 and item is deleted.

## Conclusion
On this post we saw how to use Casbin to implement authorization on REST APIs. Keep in consideration that this example can be extended combining with other authorization models like RBAC, and only changing the model and policy configuration files.

## Reference
[Authorization on FastAPI with Casbin](https://dev.to/teresafds/authorization-on-fastapi-with-casbin-41og)

[How we can manage roles and permissions using fast-API dynamically?](https://github.com/tiangolo/fastapi/issues/5676#issuecomment-1327994550)
