from __future__ import annotations

from typing import List, Dict, Optional
import random
import networkx as nx


class NarrativeMap:
    """
    Interaktywna mapa narracyjna oparta o graf skierowany (networkx.DiGraph).

    :param themes: Lista motywów przewodnich (np. ["odkupienie", "tajemnica"]).
    :type themes: list[str]
    :param locations: Lista lokalizacji możliwych w narracji.
    :type locations: list[str]
    :param characters: Lista postaci wykorzystywanych w opisach.
    :type characters: list[str]
    :param seed: Ziarno generatora losowego dla deterministyczności (None = brak deterministyczności).
    :type seed: int | None
    :raises ValueError: Gdy listy themes/locations/characters są puste.

    **Przykład**
    -------
    >>> nm = NarrativeMap(["odkupienie"], ["zamek"], ["Wędrowiec"], seed=123)
    >>> nm.build_tree(depth=2)
    >>> # 'start' jest korzeniem
    >>> "start" in nm.graph
    True
    """

    def __init__(self, themes: List[str], locations: List[str], characters: List[str], seed: Optional[int] = 42) -> None:
        if not themes or not locations or not characters:
            raise ValueError("themes, locations i characters nie mogą być puste.")
        self.themes: List[str] = themes
        self.locations: List[str] = locations
        self.characters: List[str] = characters
        self.seed: Optional[int] = seed
        self._rng = random.Random(seed)
        self.graph: nx.DiGraph = nx.DiGraph()

    def build_tree(self, depth: int = 3) -> None:
        """
        Buduje binarne drzewo decyzyjne ukorzenione w węźle ``'start'`` o zadanej głębokości.

        Każdy węzeł otrzymuje opis zdarzenia (2–3 zdania).
        Dla każdego węzła niekońcowego tworzone są dwie krawędzie (kontrastowe decyzje),
        z atrybutami ``choice``, ``risk`` i ``reward`` (1–10).

        :param depth: Głębokość drzewa (liczba krawędzi od korzenia do liścia).
        :type depth: int
        :raises ValueError: Gdy ``depth < 1``.
        :return: None
        :rtype: None

        **Przykład**
        -------
        >>> nm = NarrativeMap(["tajemnica"], ["mglista dolina"], ["Cień"], seed=7)
        >>> nm.build_tree(depth=2)
        >>> sorted(nm.graph.successors("start"))  # doctest: +ELLIPSIS
        ['start_L', 'start_R']
        """
        if depth < 1:
            raise ValueError("depth musi być >= 1.")

        # Pary kontrastowych etykiet decyzji
        decision_pairs = [
            ("zaufaj", "zdradź"),
            ("ucieknij", "staw czoła"),
            ("otwórz", "zatrzaśnij"),
            ("milcz", "wyjaw"),
            ("poświęć", "ocal"),
        ]

        # Inicjalizacja korzenia
        self.graph.clear()
        root_id = "start"
        self.graph.add_node(root_id, description=self._generate_event_description(root_id))

        # Iteracyjne rozwijanie poziomami
        frontier = [(root_id, 0)]
        dp_idx = 0  # indeks pary decyzji

        while frontier:
            node_id, lvl = frontier.pop(0)
            if lvl >= depth:
                continue  # liść

            # Dla każdego węzła niekońcowego: dwie decyzje (L/R)
            left_id = f"{node_id}_L"
            right_id = f"{node_id}_R"

            # Zapewnij istnienie węzłów z opisami
            for cid in (left_id, right_id):
                if cid not in self.graph:
                    self.graph.add_node(cid, description=self._generate_event_description(cid))

            # Wybór pary decyzji (kontrastowej) deterministycznie
            choice_left, choice_right = decision_pairs[dp_idx % len(decision_pairs)]
            dp_idx += 1

            # Losowe (deterministycznie) ryzyko/nagroda 1–10
            risk_L = self._rng.randint(1, 10)
            reward_L = self._rng.randint(1, 10)
            risk_R = self._rng.randint(1, 10)
            reward_R = self._rng.randint(1, 10)

            # Dodanie krawędzi z atrybutami
            self.graph.add_edge(node_id, left_id, choice=choice_left, risk=risk_L, reward=reward_L)
            self.graph.add_edge(node_id, right_id, choice=choice_right, risk=risk_R, reward=reward_R)

            # Rozwijamy dalej, jeśli nie osiągnęliśmy maksymalnej głębokości
            if lvl + 1 < depth:
                frontier.append((left_id, lvl + 1))
                frontier.append((right_id, lvl + 1))

    def get_path_summary(self, path: List[str]) -> Dict[str, object]:
        """
        Zwraca podsumowanie ścieżki od korzenia do liścia.

        Sumuje atrybuty ``risk`` i ``reward`` po krawędziach ścieżki
        oraz zwraca listy opisów zdarzeń i etykiet decyzji.

        :param path: Lista identyfikatorów węzłów od korzenia do liścia (np. ["start", "start_L", "start_LL"]).
        :type path: list[str]
        :raises ValueError: Gdy ścieżka ma mniej niż 1 węzeł lub nie istnieje krawędź pomiędzy kolejnymi węzłami.
        :return: Słownik z kluczami: ``events``, ``choices``, ``total_risk``, ``total_reward``, ``n_steps``.
        :rtype: dict

        **Przykład**
        -------
        >>> nm = NarrativeMap(["odkupienie"], ["zamek"], ["Wędrowiec"], seed=1)
        >>> nm.build_tree(depth=2)
        >>> path = ["start", "start_L", "start_LL"]
        >>> summary = nm.get_path_summary(path)
        >>> set(summary.keys()) == {"events", "choices", "total_risk", "total_reward", "n_steps"}
        True
        """
        if not path:
            raise ValueError("Ścieżka nie może być pusta.")

        events: List[str] = []
        choices: List[str] = []
        total_risk = 0
        total_reward = 0

        # Zbierz opisy zdarzeń węzłów
        for node_id in path:
            if node_id not in self.graph:
                raise ValueError(f"Węzeł '{node_id}' nie istnieje w grafie.")
            events.append(self.graph.nodes[node_id].get("description", ""))

        # Zbierz decyzje i sumy po krawędziach
        for u, v in zip(path[:-1], path[1:]):
            if not self.graph.has_edge(u, v):
                raise ValueError(f"Brak krawędzi {u} -> {v} w grafie.")
            edge_data = self.graph.edges[u, v]
            choices.append(edge_data.get("choice", ""))
            total_risk += int(edge_data.get("risk", 0))
            total_reward += int(edge_data.get("reward", 0))

        return {
            "events": events,
            "choices": choices,
            "total_risk": total_risk,
            "total_reward": total_reward,
            "n_steps": max(0, len(path) - 1),
        }

    def _generate_event_description(self, node_id: str) -> str:
        """
        Generuje krótki opis zdarzenia (2–3 zdania) dla węzła.

        W opisie deterministycznie mieszane są motywy, lokalizacje i postaci.
        Symuluje to wywołanie LLM.

        :param node_id: Identyfikator węzła.
        :type node_id: str
        :return: Opis zdarzenia.
        :rtype: str
        """
        # TODO: call GPT here
        theme = self.themes[self._rng.randrange(len(self.themes))]
        location = self.locations[self._rng.randrange(len(self.locations))]
        character = self.characters[self._rng.randrange(len(self.characters))]

        sentences = [
            f"W {location} {character} konfrontuje się z motywem '{theme}', który powraca niczym echo dawnych wyborów.",
            f"Węzeł {node_id} odsłania ukrytą zależność: ścieżka naprzód wymaga ceny, której jeszcze nie nazwano.",
        ]

        # Sporadycznie dodaj 3. zdanie
        if self._rng.random() < 0.5:
            twist = self._rng.choice([
                "Przysięga z przeszłości nagle zaczyna znaczyć więcej niż teraźniejszość.",
                "Cień intencji rozciąga się szerzej, niż pozwala na to pamięć.",
                "Między milczeniem a prawdą pojawia się drganie, które zmienia bieg zdarzeń.",
            ])
            sentences.append(twist)

        return " ".join(sentences)


if __name__ == "__main__":
    # Przykład użycia zgodnie z wymaganiami:
    themes = ["odkupienie", "tajemnica"]
    locations = ["opuszczony zamek", "mglista dolina"]
    characters = ["Wędrowiec", "Cień"]

    nm = NarrativeMap(themes=themes, locations=locations, characters=characters, seed=42)
    nm.build_tree(depth=3)

    # Pobierz jedną z wygenerowanych ścieżek: najdalej idąca lewą gałęzią.
    path = ["start"]
    current = "start"
    # Idź zawsze w lewo, o ile to możliwe
    while True:
        successors = sorted(nm.graph.successors(current))
        left = None
        for s in successors:
            if s.startswith(f"{current}_L"):
                left = s
                break
        if left is None:
            # jeśli nie ma lewego potomka, a jest jakikolwiek, wybierz pierwszy deterministycznie
            if successors:
                left = successors[0]
            else:
                break
        path.append(left)
        current = left
        # zakończ, gdy dotarliśmy do liścia (brak następców)
        if nm.graph.out_degree(current) == 0:
            break

    summary = nm.get_path_summary(path)

    # Wydruki: podsumowanie ścieżki
    print("=== Podsumowanie ścieżki (lewa gałąź) ===")
    print("Węzły:", " -> ".join(path))
    print("Decyzje:", " | ".join(summary["choices"]))
    print("Suma ryzyka:", summary["total_risk"])
    print("Suma nagrody:", summary["total_reward"])
    print("Liczba kroków:", summary["n_steps"])
    print("\n--- Opisy zdarzeń ---")
    for i, ev in enumerate(summary["events"], 1):
        print(f"[{i}] {ev}")

    # Demonstracja atrybutów krawędzi
    print("\n=== Krawędzie (choice, risk, reward) ===")
    for u, v, data in nm.graph.edges(data=True):
        print(f"{u} -> {v}: choice='{data['choice']}', risk={data['risk']}, reward={data['reward']}")
