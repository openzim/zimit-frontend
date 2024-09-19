from typing import Any

import pytest

from zimitfrontend.constants import ApiConfiguration
from zimitfrontend.routes.schemas import MailToSend, TaskInfo, TaskInfoFlag, ZimfarmTask
from zimitfrontend.routes.utils import (
    FAILED,
    SUCCESS,
    convert_hook_to_mail,
    get_task_info,
)


@pytest.mark.parametrize(
    "task,expected",
    [
        pytest.param(
            {
                "_id": "6341c25f-aac9-41aa-b9bb-3ddee058a0bf",
                "status": "requested",
                "config": {
                    "warehouse_path": "/other",
                    "flags": {"flag2": "value2", "flag1": "value1"},
                },
                "files": {
                    "file2.zim": {
                        "created_timestamp": "2024-09-11T13:13:36.091000Z",
                        "size": 12345,
                        "name": "file2.zim",
                    },
                    "file1.zim": {
                        "created_timestamp": "2024-09-10T13:13:36.091000Z",
                        "size": 3456,
                        "name": "file1.zim",
                    },
                    "file3.zim": {
                        "created_timestamp": "2024-09-12T13:13:36.091000Z",
                        "size": 2345,
                        "name": "file3.zim",
                    },
                },
                "notification": {"ended": {"webhook": ["bla"]}},
                "container": {"progress": {"limit": {"hit": "true"}}},
            },
            TaskInfo(
                id="6341c25f-aac9-41aa-b9bb-3ddee058a0bf",
                download_link="https://s3.us-west-1.wasabisys.com/org-kiwix-zimit/zim/other"
                "/file1.zim",
                limit_hit=True,
                has_email=True,
                status="requested",
                flags=[
                    TaskInfoFlag(name="flag1", value="value1"),
                    TaskInfoFlag(name="flag2", value="value2"),
                ],
                progress=0,
            ),
            id="full",
        ),
        pytest.param(
            {
                "_id": "6341c25f-aac9-41aa-b9bb-3ddee058a0bf",
                "config": {"warehouse_path": "/other", "flags": {}},
                "status": "blu",
            },
            TaskInfo(
                id="6341c25f-aac9-41aa-b9bb-3ddee058a0bf",
                download_link=None,
                limit_hit=False,
                has_email=False,
                status="blu",
                flags=[],
                progress=0,
            ),
            id="simple",
        ),
        pytest.param(
            {
                "_id": "6341c25f-aac9-41aa-b9bb-3ddee058a0bf",
                "config": {"warehouse_path": "/other", "flags": {}},
                "container": {"progress": {"limit": {"hit": "false"}}},
                "status": "bla",
            },
            TaskInfo(
                id="6341c25f-aac9-41aa-b9bb-3ddee058a0bf",
                download_link=None,
                limit_hit=False,
                has_email=False,
                status="bla",
                flags=[],
                progress=0,
            ),
            id="limit_not_hit",
        ),
    ],
)
def test_convert_zimfarm_task_to_info(task: Any, expected: TaskInfo):
    assert get_task_info(task) == expected


DEFAULT_HOOK_TASK = ZimfarmTask.model_validate(
    {
        "_id": "6341c25f-aac9-41aa-b9bb-3ddee058a0bf",
        "status": "requested",
        "config": {
            "warehouse_path": "/other",
            "flags": {"url": "https://www.acme.com"},
        },
        "files": {
            "file2.zim": {
                "created_timestamp": "2024-09-11T13:13:36.091000Z",
                "size": 12345,
                "name": "file2.zim",
            },
            "file1.zim": {
                "created_timestamp": "2024-09-10T13:13:36.091000Z",
                "size": 6543,
                "name": "file1.zim",
            },
        },
        "notification": {"ended": {"webhook": ["bla"]}},
        "container": {"progress": {"limit": {"hit": "true"}}},
        "flags": {"flag2": "value2", "flag1": "value1"},
    }
)


@pytest.mark.parametrize(
    "token,target,lang,task,task_status,expected",
    [
        pytest.param(
            ApiConfiguration.hook_token,
            "bob@acme.com",
            "en",
            DEFAULT_HOOK_TASK,
            "requested",
            MailToSend(
                status=SUCCESS,
                target="bob@acme.com",
                subject="Youzim.it task 6341c requested",
                body=r"""<html  lang="en">
<body>

<h2>ZIM requested!</h2>
<p>Your ZIM request of <a href="https://www.acme.com">https://www.acme.com</a> has """
                r"""been recorded.</p>
<p>You can follow the status of this request at <a href="""
                r""""https://zimit.kiwix.org/#/request/6341c25f-aac9-41aa-b9bb-3ddee058a0bf">"""
                r"""https://zimit.kiwix.org/#/request/6341c25f-aac9-41aa-b9bb-3ddee058a0bf</a>.</p>
<p>We&#39;ll send you another email once your ZIM file is ready to download.</p>





</body>
</html>""",
            ),
            id="requested",
        ),
        pytest.param(
            ApiConfiguration.hook_token,
            "bob@acme.com",
            "en",
            DEFAULT_HOOK_TASK,
            "succeeded",
            MailToSend(
                status=SUCCESS,
                target="bob@acme.com",
                subject="Youzim.it task 6341c succeeded",
                body=r"""<html  lang="en">
<body>



<h2>ZIM is ready!</h2>
<p>Your ZIM request of <a href="https://www.acme.com">https://www.acme.com</a> has """
                r"""completed.</p>
<p>Here it is:</p>
<ul>
<li><a href="https://s3.us-west-1.wasabisys.com/org-kiwix-zimit/zim/other/file2.zim"""
                r"""">file2.zim</a> (12.06 KiB)</li><li>"""
                r"""<a href="https://s3.us-west-1.wasabisys.com/org-kiwix-zimit"""
                r"""/zim/other/file1.zim">file1.zim</a> (6.39 KiB)</li>
</ul>

<p>ZIM is unfortunately incomplete because you have reached the limits (4 GiB or """
                r"""2 hours) allowed for free crawling. <a href="https://www.kiwix.org/en/contact/">"""
                r"""Contact us</a> to help us purchase additional server space for """
                r"""you.</p>



</body>
</html>""",
            ),
            id="succeeded",
        ),
        pytest.param(
            ApiConfiguration.hook_token,
            "bob@acme.com",
            "en",
            DEFAULT_HOOK_TASK,
            "failed",
            MailToSend(
                status=SUCCESS,
                target="bob@acme.com",
                subject="Youzim.it task 6341c failed",
                body=r"""<html  lang="en">
<body>





<h2>Your ZIM request has failed!</h2>
<p>We are really sorry.</p>
<p>This might be due to an error with the URL you entered ("""
                r"""<a href="https://www.acme.com">https://www.acme.com</a>) or """
                r"""additional settings missing / failing. Please double check and """
                r"""<a href="https://zimit.kiwix.org">try again</a>.</p>
<p>You can check the settings you used at <a href="https://zimit.kiwix.org/#/request/"""
                r"""6341c25f-aac9-41aa-b9bb-3ddee058a0bf">"""
                r"""https://zimit.kiwix.org/#/request/6341c25f-aac9-41aa-b9bb-3ddee058a0bf"""
                r"""</a>.</p>
</body>
</html>""",
            ),
            id="failed",
        ),
        pytest.param(
            ApiConfiguration.hook_token,
            "bob@acme.com",
            "en",
            DEFAULT_HOOK_TASK,
            "bad_status",
            MailToSend(
                status=SUCCESS,
                target=None,
                subject=None,
                body=None,
            ),
            id="bad_status",
        ),
        pytest.param(
            ApiConfiguration.hook_token,
            "",
            "en",
            DEFAULT_HOOK_TASK,
            "succeeded",
            MailToSend(
                status=FAILED,
                target=None,
                subject=None,
                body=None,
            ),
            id="bad_target1",
        ),
        pytest.param(
            ApiConfiguration.hook_token,
            None,
            "en",
            DEFAULT_HOOK_TASK,
            "succeeded",
            MailToSend(
                status=FAILED,
                target=None,
                subject=None,
                body=None,
            ),
            id="bad_target2",
        ),
        pytest.param(
            "bad_token",
            "bob@acme.com",
            "en",
            DEFAULT_HOOK_TASK,
            "succeeded",
            MailToSend(
                status=FAILED,
                target=None,
                subject=None,
                body=None,
            ),
            id="bad_token",
        ),
        pytest.param(
            ApiConfiguration.hook_token,
            "bob@acme.com",
            "en",
            None,
            "succeeded",
            MailToSend(
                status=FAILED,
                target=None,
                subject=None,
                body=None,
            ),
            id="bad_task",
        ),
    ],
)
def test_convert_hook_to_mail(
    token: str | None,
    target: str | None,
    lang: str,
    task: ZimfarmTask | None,
    task_status: str,
    expected: MailToSend,
):
    if task:
        task.status = task_status
    result = convert_hook_to_mail(
        token=token,
        target=target,
        lang=lang,
        task=task,
    )
    assert result.status == expected.status
    assert result.target == expected.target
    assert result.subject == expected.subject
    assert result.body == expected.body