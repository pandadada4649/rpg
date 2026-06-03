class Party:
    def __init__(self, leader):
        self.members = [leader]

    @property
    def leader(self):
        return self.members[0]

    def add_member(self, member):
        if len(self.members) >= 4:
            print("パーティは4人までです！")
            return False
        self.members.append(member)
        print(f"🤝 {member.name}がパーティに加わった！")
        return True

    def is_alive(self) -> bool:
        return any(m.is_alive for m in self.members)

    def show_status(self):
        for member in self.members:
            member.show_status()
            print()

    def alive_members(self):
        return [m for m in self.members if m.is_alive]