Feature: Todo 관리
  Todo 생성, 조회, 수정, 삭제 기능

  Scenario: Todo 생성
    When Todo를 생성한다
    Then Todo가 정상적으로 생성된다
    And 생성된 Todo를 DB에서 조회할 수 있다

  Scenario: 빈 목록 조회
    When Todo 목록을 조회한다
    Then 빈 리스트가 반환된다

  Scenario: Todo 목록 조회
    Given 2개의 Todo가 존재한다
    When Todo 목록을 조회한다
    Then 2개의 Todo가 반환된다

  Scenario: Todo 삭제
    Given Todo가 생성되어 있다
    When Todo를 삭제한다
    Then Todo가 삭제된다
    And 삭제된 Todo를 DB에서 조회할 수 없다

  Scenario: Todo 업데이트
    Given Todo가 생성되어 있다
    When Todo의 완료 상태를 true로 변경한다
    Then Todo가 정상적으로 업데이트된다
    And DB에서 조회한 Todo의 완료 상태가 true이다
