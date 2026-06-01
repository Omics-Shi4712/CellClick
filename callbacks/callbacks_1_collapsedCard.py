"""
@File        : callbacks_1_collapsedCard.py
@Author      : Min Dai, shi4712
@Date        : 2022/8/29 15:19
@Description : define the callbacks to render Collapse Card components in Cell Click
"""
from numpy.core.shape_base import block

from callbacks.callbacks_0_returnFresh import *


# define the behaviors of collapseCard
@callback(
    Output(
        {"card_name": MATCH, "type": "collapse"},
        "is_open"
    ),
    inputs=dict(
        buttonClickNum=Input(
            {"card_name": MATCH, "type": "card_button"},
            "n_clicks"
        ),
        collapseStats=State(
            {"card_name": MATCH, "type": "collapse"},
            "is_open"
        )
    ),
    prevent_initial_call=True,
)
def collapseCard(buttonClickNum, collapseStats):
    return not collapseStats


# @callback(
#     Output(
#         {"card_name": MATCH, "form_name": ALL, "type": "form_button"},
#         "active",
#     ),
#     Output(
#         {"card_name": MATCH, "form_name": ALL, "type": "document_button"},
#         "active",
#     ),
#     Output(
#         {"card_name": MATCH, "form_name": ALL},
#         "style"
#     ),
#     inputs=dict(
#         userSessionId=Input('User Session ID', 'data'),
#         buttonIDs=State(
#             {"card_name": MATCH, "form_name": ALL, "type": "form_button"},
#             "id",
#         ),
#         buttonClickNums=Input(
#             {"card_name": MATCH, "form_name": ALL, "type": "form_button"},
#             "n_clicks",
#         ),
#         activeValues=State(
#             {"card_name": MATCH, "form_name": ALL, "type": "form_button"},
#             "active",
#         ),
#         formStyles=State(
#             {"card_name": MATCH, "form_name": ALL},
#             "style"
#         ),
#     ),
# )
# def returnCollapseCardContent(userSessionId, buttonIDs, buttonClickNums, activeValues, formStyles):
#     def initCollapseCardContent():
#         for style in formStyles[1:]:
#             style["display"] = "none"
#
#         initActiveValues = [False]*len(buttonClickNums)
#
#         return initActiveValues, initActiveValues, formStyles
#
#     def returnCollapseCardContentBasedButton(buttonIndex):
#         newActiveValues, newActiveValues, newFormStyles = initCollapseCardContent()
#         newActiveValues[buttonIndex] = True
#
#         for formStyle in newFormStyles:
#             formStyle["display"] = "none"
#         if not userSessionId and not (ctxId["card_name"] == "Data Settings" and buttonIndex in [0, 1, 2]):
#             # 0 button in Brief Summary and Settings is used for data upload
#             newFormStyles[0]["display"] = "block"
#         else:
#             newFormStyles[buttonIndex + 1]["display"] = "block"
#
#         return newActiveValues, newActiveValues, newFormStyles
#
#     ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)
#     if ctxIdStr == "":
#         return initCollapseCardContent()
#     elif ctxIdStr == "User Session ID":
#         if userSessionId is None:
#             return initCollapseCardContent()
#         else:
#             if True in activeValues:
#                 buttonIndex = activeValues.index(True)
#                 return returnCollapseCardContentBasedButton(buttonIndex=buttonIndex)
#             else:
#                 raise PreventUpdate
#     else:
#         ctxId = json.loads(ctxIdStr)
#         formNames = [buttonID["form_name"] for buttonID in buttonIDs]
#         formName = ctxId["form_name"]
#         buttonIndex = formNames.index(formName)
#         return returnCollapseCardContentBasedButton(buttonIndex=buttonIndex)


@callback(
    Output(
        {"card_name": ALL, "form_name": ALL, "type": "form_button"},
        "active",
    ),
    Output(
        {"card_name": ALL, "form_name": ALL, "type": "document_button"},
        "active",
    ),
    Output(
        {"card_name": ALL, "form_name": ALL},
        "style"
    ),
    inputs=dict(
        userSessionId=Input('User Session ID', 'data'),
        buttonIDs=State(
            {"card_name": ALL, "form_name": ALL, "type": "form_button"},
            "id",
        ),
        buttonClickNums=Input(
            {"card_name": ALL, "form_name": ALL, "type": "form_button"},
            "n_clicks",
        ),
        activeValues=State(
            {"card_name": ALL, "form_name": ALL, "type": "form_button"},
            "active",
        ),
        formIDs=State(
            {"card_name": ALL, "form_name": ALL},
            "id"
        ),
        formStyles=State(
            {"card_name": ALL, "form_name": ALL},
            "style"
        ),
    ),
)
def returnCollapseCardContent(userSessionId, buttonIDs, buttonClickNums, activeValues, formIDs, formStyles):
    def initCollapseCardContent():
        for style in formStyles:
            style["display"] = "none"

        initActiveValues = [False]*len(buttonClickNums)

        return initActiveValues, initActiveValues, formStyles

    def returnCollapseCardContentBasedButton(card_name, form_name, error=True):
        newActiveValues, newActiveValues, newFormStyles = initCollapseCardContent()


        for index, buttonID in zip(range(0, len(newActiveValues)), buttonIDs):
            if buttonID["card_name"] == card_name and buttonID["form_name"] == form_name:
                newActiveValues[index] = True
                break

        if error:
            if not (card_name == "Data Settings" and form_name == "Upload"):
                form_name = "error"
        for newFormStyle, formID in zip(newFormStyles, formIDs):
            if formID["card_name"] == card_name and formID["form_name"] == form_name:
                newFormStyle["display"] = "block"
                break

        return newActiveValues, newActiveValues, newFormStyles

    ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)
    if ctxIdStr == "":
        return initCollapseCardContent()
    elif ctxIdStr == "User Session ID":
        if True in activeValues:
            for activeValue, buttonID in zip(activeValues, buttonIDs):
                if activeValue:
                    card_name = buttonID["card_name"]
                    form_name = buttonID["form_name"]
                    return returnCollapseCardContentBasedButton(
                        card_name=card_name, form_name=form_name,
                        error=userSessionId is None,
                    )
        else:
            return initCollapseCardContent()
    else:
        ctxId = json.loads(ctxIdStr)
        return returnCollapseCardContentBasedButton(
            card_name=ctxId["card_name"], form_name=ctxId["form_name"],
            error=userSessionId is None,
        )
