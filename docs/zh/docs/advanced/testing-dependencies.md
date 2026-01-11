# 使用覆盖项测试依赖项 { #testing-dependencies-with-overrides }

## 在测试期间覆盖依赖项 { #overriding-dependencies-during-testing }

有些场景下，你可能需要在测试期间覆盖依赖项。

你不希望运行原有依赖项（及其可能包含的任何子依赖项）。

相反，你希望提供一个仅在测试期间使用的不同依赖项（可能只用于某些特定测试），并提供一个值，以便在原依赖项的值被使用的地方使用该值。

### 用例：外部服务 { #use-cases-external-service }

例如，你可能有一个需要调用的外部身份验证提供方。

你向它发送一个 token，它会返回一个已认证的用户。

这个提供方可能会按请求向你收费，并且调用它可能会比在测试中使用固定的 mock 用户花费更多时间。

你可能只想测试一次外部提供方，但不一定要在每个运行的测试中都调用它。

在这种情况下，你可以覆盖调用该提供方的依赖项，并仅在测试中使用一个返回 mock 用户的自定义依赖项。

### 使用 `app.dependency_overrides` 属性 { #use-the-app-dependency-overrides-attribute }

对于这些情况，你的 **FastAPI** 应用有一个属性 `app.dependency_overrides`，它是一个简单的 `dict`。

要在测试时覆盖依赖项，你把原依赖项（一个函数）作为键，把你的依赖项覆盖（另一个函数）作为值。

然后 **FastAPI** 就会调用该覆盖项，而不是原依赖项。

{* ../../docs_src/dependency_testing/tutorial001_an_py310.py hl[26:27,30] *}

/// tip | 提示

你可以为 **FastAPI** 应用中任意位置使用的依赖项设置依赖项覆盖。

原依赖项可以用于*路径操作函数*、*路径操作装饰器*（当你不使用返回值时）、`.include_router()` 调用等。

FastAPI 仍然可以覆盖它。

///

然后，你可以通过将 `app.dependency_overrides` 设置为空 `dict` 来重置你的覆盖项（移除它们）：

```Python
app.dependency_overrides = {}
```

/// tip | 提示

如果你只想在某些测试期间覆盖依赖项，你可以在测试开始时（在测试函数内）设置覆盖，并在结束时（在测试函数结尾）重置它。

///
