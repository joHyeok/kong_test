import unreal

def SelectedActor():
    EditorSystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    global selected_actors
    selected_actors = EditorSystem.get_selected_level_actors()
    return selected_actors

def ChangeSelectedActor():
    #실행취소 가능하도록
    with unreal.ScopedEditorTransaction("Change Actors") as trans:
        EditorSystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        copy_actors = EditorSystem.get_selected_level_actors()

    #복사할 액터가 1개가 아니라면, 선택된 액터가 0개라면 나가기
        if(len(copy_actors) != 1 or len(selected_actors) == 0):
            unreal.log_warning('Check Selected Actors or Change Actor')
            return

    #복사할 액터
        change_actor = copy_actors[0]

    #선택된 액터들 for문으로 복사 액터 만들고 제거하기
        for i in selected_actors:
            NewActor = EditorSystem.duplicate_actor(change_actor)
            NewActor.set_actor_location_and_rotation(
                i.get_actor_location(), i.get_actor_rotation(), False, False)
            i.destroy_actor()

def AddGroup(self):
    with unreal.ScopedEditorTransaction("Add Group") as trans:
        EditorSystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        ForGroup_Selected_Actors = EditorSystem.get_selected_level_actors()
        unreal.ActorGroupingUtils.group_actors(self, ForGroup_Selected_Actors)


def MakeCircle(radius):
    with unreal.ScopedEditorTransaction("Make circle") as trans:
        EditorSystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        ForCircle_Selected_Actors = EditorSystem.get_selected_level_actors()

        #뿌려야할 개수
        SelectedActorLength = len(ForCircle_Selected_Actors) - 1
        if(SelectedActorLength <= 0):
            unreal.log_warning('Check Actor Num')
            return
        
        #중심 위치
        CirclePoint = ForCircle_Selected_Actors[0].get_actor_location()

        #액터당 각도
        Angle = 360.0 / SelectedActorLength

        for i in range(SelectedActorLength):
            #현재 계산할 액터 카운트
            currentActorCount = i + 1
            
            #각도
            Dir = unreal.Vector2D(1, 0).get_rotated(Angle * i)

            #반지름 곱한 2d 벡터
            DirVector2D = unreal.Vector2D(Dir.x * radius, Dir.y * radius)

            #위치 수정
            ForCircle_Selected_Actors[currentActorCount].set_actor_location(
                CirclePoint + unreal.Vector(DirVector2D.x, DirVector2D.y, 0), False, False)
    