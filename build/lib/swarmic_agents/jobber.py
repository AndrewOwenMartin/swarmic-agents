from dataclasses import dataclass
import json
from pathlib import Path
from typing import TypedDict
from uuid import UUID, uuid4
import chat
from datetime import datetime, UTC


@dataclass
class Job:
    name: str
    prompt: list[Path]

    @property
    def agent_dir(self) -> Path:
        return Path("agents") / self.name

    @property
    def inbox(self) -> Path:
        return self.agent_dir / "inbox"

    @property
    def outbox(self) -> Path:
        return self.agent_dir / "outbox"

    @property
    def prompt_dir(self) -> Path:
        return self.agent_dir / "prompt"

    def get_payload(self, inbox_item: Path) -> dict:
        texts = []
        for prompt_file in self.prompt:
            texts.append(prompt_file.read_text())
        texts.append(inbox_item.read_text())
        return chat.make_payload(texts=texts)

    def create_directories(self):
        for directory in [self.inbox, self.outbox, self.prompt_dir]:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {directory}")


jobs = [Job(name="proposer", prompt=[Path("SKILL.md")])]


def init_jobs():
    for job in jobs:
        job.create_directories()


class JobInfo(TypedDict):
    id: UUID
    start: datetime
    end: datetime
    agent: str


class UUIDEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, UUID):
            return str(o)
        return json.JSONEncoder.default(self, o)


def write_job_db(job_info: JobInfo):
    job_db_path = Path("job_db.jsonl")
    with job_db_path.open("a") as f:
        f.write(json.dumps(job_info, cls=UUIDEncoder) + "\n")


def run_jobber():
    for job in jobs:
        for inbox_item in job.inbox.iterdir():
            payload = job.get_payload(inbox_item)
            start = datetime.now(tz=UTC)
            response = chat.send_payload(payload)
            end = datetime.now(tz=UTC)
            job_id = uuid4()
            write_job_db(
                job_info=JobInfo(id=job_id, start=start, end=end, agent=job.name)
            )
            job_out_path = job.outbox / f"{job_id}.json"
            with job_out_path.open("w") as f:
                json.dump(response, f)


if __name__ == "__main__":
    init_jobs()
    run_jobber()
