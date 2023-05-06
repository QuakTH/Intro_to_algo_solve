# implementation of counting sort


from intro_to_algo_solve.lecture7.counting_sort import CountingSort


class RadixSort(CountingSort):
    """Class containing methods for radix sort."""

    def __init__(self, max_key: int, divisor: int) -> None:
        super().__init__(max_key)
        self.divisor = divisor  # A value for radix sort

    def sort(self) -> None:
        """Do a radix sort on `self.nodes`."""
        self.reset_buckets()
        same_share_count = 0
        for node in self.nodes:
            before_share = node.share
            node.remainder = node.share % self.divisor
            node.share //= self.divisor
            self.bucket[node.remainder] += 1

            if before_share == node.share:
                same_share_count += 1
        if same_share_count == len(self.nodes):
            return

        self.cum_bucket[0] = self.bucket[0]
        for idx in range(1, len(self.cum_bucket)):
            self.cum_bucket[idx] = self.cum_bucket[idx - 1] + self.bucket[idx]

        sorted_nodes = [None for _ in range(len(self.nodes))]
        for node in reversed(self.nodes):
            key = node.remainder
            sorted_nodes[self.cum_bucket[key] - 1] = node
            self.cum_bucket[key] -= 1
        self.nodes = sorted_nodes

        self.sort()
