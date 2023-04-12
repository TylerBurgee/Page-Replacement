"""
Author: Tyler J. Burgee
Date: 12 April 2023
Course: CIS 390 - Operating Systems
"""

class PageReplacer:
    """Class for replacing pages in main memory"""

    def __init__(self, page_frames: int) -> None:
        """Defines the constructor for a PageReplacer object"""
        self.page_frames = [None]*page_frames

    def _insert_to_empty_frame_(self, page: int) -> bool:
        """If an empty frame is found, the given page is inserted into that frame"""
        inserted = False
        for x, frame in enumerate(self.page_frames):
            if frame is None:
                self.page_frames[x] = page
                inserted = True
                break
        return inserted

    def _detect_hit_(self, page: int) -> bool:
        """Returns true if a given page is found in a main memory frame"""
        if page in self.page_frames:
            print("Hit  ({}):".format(page), self.page_frames)
            return True
        return False

    def _get_ref_distances_(self, pages: list):
        """Calculates the distances of page references"""
        distances = [(page, pages.index(page)) for page in set(pages)]
        distances.sort(key=lambda tup: tup[1], reverse=True)
        return distances

    def fifo(self, page_ref: list) -> None:
        """Replaces page according to first in first out algorithm"""
        queue = []
        page_faults = 0
        print("Pages Frames:", self.page_frames)

        for page in page_ref:
            hit = self._detect_hit_(page)
            if hit:
                continue

            inserted = self._insert_to_empty_frame_(page)
            if inserted:
                queue.append(page)

            # REPLACE A PAGE REFERENCE WITH THE NEW PAGE REFERENCE
            if page not in queue:
                popped_frame = queue.pop(0)
                queue.append(page)
                for x, frame in enumerate(self.page_frames):
                    if frame == popped_frame:
                        self.page_frames[x] = page
                        break

            print("Miss ({}):".format(page), self.page_frames)
            page_faults += 1

        return page_faults

    def lru(self, page_ref: list) -> None:
        """Replaces page according to least recently used algorithm"""
        lru = []
        page_faults = 0
        print("Pages Frames:", self.page_frames)

        for page in page_ref:
            inserted = False

            # UPDATE LEAST RECENTLY USED PAGES
            if page not in lru:
                lru.append(page)
            else:
                lru.remove(page)
                lru.append(page)

            hit = self._detect_hit_(page)
            if hit:
                continue

            inserted = self._insert_to_empty_frame_(page)

            # REPLACE A PAGE REFERENCE WITH THE NEW PAGE REFERENCE
            if not inserted:
                popped_frame = lru.pop(0)
                for x, frame in enumerate(self.page_frames):
                    if frame == popped_frame:
                        self.page_frames[x] = page
                        break

            print("Miss ({}):".format(page), self.page_frames)
            page_faults += 1

        return page_faults

    def optimal(self, page_ref: list) -> None:
        """Replaces page according to optimal algorithm"""
        page_faults = 0
        pages_remaining = [page for page in page_ref]
        print("Pages Frames:", self.page_frames)

        for page in page_ref:
            inserted = False

            hit = self._detect_hit_(page)
            if hit:
                pages_remaining.pop(0)
                continue

            inserted = self._insert_to_empty_frame_(page)

            # REPLACE A PAGE REFERENCE WITH THE NEW PAGE REFERENCE
            if not inserted:
                page_needed = True
                for x, frame in enumerate(self.page_frames):
                    # CHECK IF PAGE IN MAIN MEMORY WILL NO LONGER BE USED
                    if frame not in pages_remaining:
                        self.page_frames[x] = page
                        page_needed = False
                # FIND THE PAGE THAT WILL NOT BE USED FOR THE LONGEST TIME IN THE FUTURE
                if page_needed:
                    distances = self._get_ref_distances_(pages_remaining)
                    i = 0
                    while True:
                        if distances[i][0] in self.page_frames:
                            self.page_frames[self.page_frames.index(distances[i][0])] = page
                            break
                        else:
                            i += 1

            print("Miss ({}):".format(page), self.page_frames)
            pages_remaining.pop(0)
            page_faults += 1

        return page_faults

if __name__ == '__main__':
    page_ref = [7,0,1,2,0,3,0,4,2,3,0,3,0,3,2,1,2,0,1,7,0,1]

    print("-"*8, "First In First Out", "-"*8)
    print("Reference String:", page_ref)
    pr = PageReplacer(3)
    page_faults = pr.fifo(page_ref)
    print("Total Page Faults:", page_faults)
    print("-"*35)

    print()

    print("-"*8, "Least Recently Used", "-"*8)
    print("Reference String:", page_ref)
    pr = PageReplacer(3)
    page_faults = pr.lru(page_ref)
    print("Total Page Faults:", page_faults)
    print("-"*35)

    print()

    print("-"*14, "Optimal", "-"*14)
    print("Reference String:", page_ref)
    pr = PageReplacer(3)
    page_faults = pr.optimal(page_ref)
    print("Total Page Faults:", page_faults)
    print("-"*35)
